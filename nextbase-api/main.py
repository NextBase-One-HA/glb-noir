"""
NextBase mandatory canonical gateway: injects local CANONICAL into every AI-bound request.
Upstream AI router base URL: TRANSLATE_UPSTREAM_URL (see Cloud Run env; never hardcode secrets).
"""
from __future__ import annotations

import os
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict

# Optional gate headers — values only from environment (never committed).
NB_GATE_HEADER_NAME = os.getenv("NB_GATE_HEADER_NAME", "X-NB-Gate-Token")
NB_GATE_TOKEN = os.getenv("NB_GATE_TOKEN", "")


def _canonical_docs_paths() -> tuple[Path, Path]:
    """Resolve repo `docs/` (monorepo) or `docs/` next to this file (container)."""
    here = Path(__file__).resolve().parent
    monorepo_docs = here.parent / "docs"
    local_docs = here / "docs"
    if (monorepo_docs / "NEXTBASE_SYSTEM_CANONICAL.md").is_file():
        base = monorepo_docs
    elif (local_docs / "NEXTBASE_SYSTEM_CANONICAL.md").is_file():
        base = local_docs
    else:
        base = monorepo_docs
    return (
        base / "NEXTBASE_SYSTEM_CANONICAL.md",
        base / "SYSTEM_INVENTORY.md",
    )


def load_canonical_context() -> str:
    """Load merged canonical text. Missing files => physical failure (caller must surface)."""
    p1, p2 = _canonical_docs_paths()
    parts: list[str] = []
    for p in (p1, p2):
        if not p.is_file():
            raise FileNotFoundError(f"CANONICAL MISSING (required): {p}")
        parts.append(p.read_text(encoding="utf-8"))
    return "\n\n---\n\n".join(parts)


app = FastAPI(title="NextBase API — Mandatory Gateway", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(",") if os.getenv("ALLOWED_ORIGINS") else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup_verify_canonical() -> None:
    """Stop process at boot if canonical files are absent."""
    load_canonical_context()


class GatewayPayload(BaseModel):
    model_config = ConfigDict(extra="allow")

    prompt: str = ""
    # Forward-through fields for ai-router /translate shape
    target: str = ""
    caller_id: str = "prod"
    model: str | None = None


async def forward_to_ai_router(enforced_prompt: str, payload: GatewayPayload) -> dict:
    base = (os.getenv("TRANSLATE_UPSTREAM_URL") or "").rstrip("/")
    if not base:
        raise HTTPException(
            status_code=500,
            detail="TRANSLATE_UPSTREAM_URL is not set; cannot forward to ai-router",
        )
    body = payload.model_dump(exclude_none=True)
    body.pop("prompt", None)
    body["text"] = enforced_prompt

    url = f"{base}/gateway"
    async with httpx.AsyncClient(timeout=120.0) as client:
        r = await client.post(url, json=body)
    try:
        data = r.json()
    except Exception:
        data = {"raw": r.text, "upstream_status": r.status_code}
    if r.is_success:
        return data
    raise HTTPException(status_code=r.status_code, detail=data)


def _check_gate(request: Request) -> None:
    if not NB_GATE_TOKEN:
        return
    sent = request.headers.get(NB_GATE_HEADER_NAME) or ""
    if sent != NB_GATE_TOKEN:
        raise HTTPException(status_code=403, detail="Gateway token mismatch or missing")


@app.post("/gateway")
async def mandatory_gateway(request: Request, payload: GatewayPayload):
    # A. 正本の強制注入 (reload every request — no trust in remote history)
    _check_gate(request)
    canonical_text = load_canonical_context()
    original_prompt = payload.prompt
    enforced_prompt = (
        f"### SYSTEM_CANONICAL_LAW ###\n{canonical_text}\n\n"
        f"### USER_REQUEST ###\n{original_prompt}"
    )

    # B. securityLevel 判定 (LEVEL 1 = 監査モード)
    if "STATE: HOLD" in canonical_text or "STATE: INVALID" in canonical_text:
        return {
            "status": "HOLD",
            "message": "Physical inventory mismatch detected. Action required by NORI.",
            "required_action": "Update environment variables or rotate keys.",
        }

    # C. ai-router への物理転送
    return await forward_to_ai_router(enforced_prompt, payload)


@app.get("/health")
def health():
    return {"ok": True, "service": "nextbase-api"}
