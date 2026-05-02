"""
NextBase mandatory gateway (執行官プロトコル): every request re-attaches the latest CANONICAL
to the prompt head. Upstream: TRANSLATE_UPSTREAM_URL only (no TRANSLATE_PROXY_URL).

Load order:
  1) NEXTBASE_CANONICAL_URL (optional external / dynamic GET)
  2) Internal static: NEXTBASE_SYSTEM_CANONICAL.md + SYSTEM_INVENTORY.md

Fail-safe: any load failure => securityLevel=1 and HOLD (process keeps running; no crash-loop).
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

CANONICAL_FETCH_TIMEOUT = float(os.getenv("NEXTBASE_CANONICAL_FETCH_TIMEOUT", "15"))


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


async def load_canonical_context() -> tuple[str | None, str | None]:
    """
    Merge canonical from URL (if set) then internal static files.
    Returns (text, error). If error is set => gateway must HOLD (securityLevel=1); no exception.
    """
    parts: list[str] = []
    url = (os.getenv("NEXTBASE_CANONICAL_URL") or "").strip()
    if url:
        try:
            async with httpx.AsyncClient(timeout=CANONICAL_FETCH_TIMEOUT) as client:
                r = await client.get(url)
            if r.status_code != 200:
                return None, f"NEXTBASE_CANONICAL_URL HTTP {r.status_code}"
            parts.append(r.text)
        except Exception as e:
            return None, f"NEXTBASE_CANONICAL_URL fetch failed: {e!s}"

    p1, p2 = _canonical_docs_paths()
    for p in (p1, p2):
        if not p.is_file():
            return None, f"CANONICAL MISSING (required): {p}"
        parts.append(p.read_text(encoding="utf-8"))

    return "\n\n---\n\n".join(parts), None


def _hold_inventory() -> dict:
    return {
        "status": "HOLD",
        "securityLevel": 1,
        "message": "Physical inventory mismatch detected. Action required by NORI.",
        "required_action": "Update environment variables or rotate keys.",
    }


def _hold_load(reason: str) -> dict:
    return {
        "status": "HOLD",
        "securityLevel": 1,
        "message": "Canonical load failure — execution halted.",
        "required_action": reason,
    }


app = FastAPI(title="NextBase API — Mandatory Gateway", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(",") if os.getenv("ALLOWED_ORIGINS") else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GatewayPayload(BaseModel):
    model_config = ConfigDict(extra="allow")

    prompt: str = ""
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
    # Stateless: reload canonical every request (no trust in AI/history).
    _check_gate(request)
    canonical_text, load_err = await load_canonical_context()
    if load_err or not canonical_text:
        return _hold_load(load_err or "Unknown canonical error")

    original_prompt = payload.prompt
    enforced_prompt = (
        f"### SYSTEM_CANONICAL_LAW ###\n{canonical_text}\n\n"
        f"### USER_REQUEST ###\n{original_prompt}"
    )

    # Inventory audit (PASS required before forward)
    if "STATE: HOLD" in canonical_text or "STATE: INVALID" in canonical_text:
        return _hold_inventory()

    # PASS -> upstream only
    return await forward_to_ai_router(enforced_prompt, payload)


@app.get("/health")
def health():
    return {"ok": True, "service": "nextbase-api", "protocol": "NEXTBASE_API_GATEWAY_FIXED"}
