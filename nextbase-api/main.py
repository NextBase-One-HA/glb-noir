"""
NextBase mandatory gateway: stateless canonical + inventory injection per request.
Upstream: TRANSLATE_UPSTREAM_URL -> POST .../gateway only. No header-token gate; no proxy URL.

Room/TTL: not handled here. No ai-router server-side state; forward is stateless HTTP only.
"""
from __future__ import annotations

import os
from pathlib import Path

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict

CANONICAL_FETCH_TIMEOUT = float(os.getenv("NEXTBASE_CANONICAL_FETCH_TIMEOUT", "15"))


def _docs_base_dir() -> Path:
    here = Path(__file__).resolve().parent
    monorepo_docs = here.parent / "docs"
    local_docs = here / "docs"
    if (monorepo_docs / "NEXTBASE_SYSTEM_CANONICAL.md").is_file():
        return monorepo_docs
    if (local_docs / "NEXTBASE_SYSTEM_CANONICAL.md").is_file():
        return local_docs
    return monorepo_docs


def _path_canonical_local() -> Path:
    return _docs_base_dir() / "NEXTBASE_SYSTEM_CANONICAL.md"


def _path_inventory_local() -> Path:
    return _docs_base_dir() / "SYSTEM_INVENTORY.md"


async def canonical_loader() -> tuple[str | None, str | None]:
    """
    NEXTBASE_CANONICAL_URL (optional) then local NEXTBASE_SYSTEM_CANONICAL.md.
    Returns (text, error). Error => gateway HOLD; never log body or secrets.
    """
    parts: list[str] = []
    url = (os.getenv("NEXTBASE_CANONICAL_URL") or "").strip()
    if url:
        try:
            async with httpx.AsyncClient(timeout=CANONICAL_FETCH_TIMEOUT) as client:
                r = await client.get(url)
            if r.status_code != 200:
                return None, "canonical_url_http_error"
            parts.append(r.text)
        except Exception:
            return None, "canonical_url_fetch_error"

    local = _path_canonical_local()
    if not local.is_file():
        return None, "canonical_local_missing"
    parts.append(local.read_text(encoding="utf-8"))
    return "\n\n---\n\n".join(parts), None


async def inventory_loader() -> tuple[str | None, str | None]:
    """Local SYSTEM_INVENTORY.md only."""
    p = _path_inventory_local()
    if not p.is_file():
        return None, "inventory_local_missing"
    return p.read_text(encoding="utf-8"), None


def security_level_hold(combined_audit_text: str) -> bool:
    """True => HOLD (no upstream forward)."""
    if "STATE: HOLD" in combined_audit_text:
        return True
    if "STATE: INVALID" in combined_audit_text:
        return True
    return False


def _hold(*, reason: str) -> dict:
    out: dict = {"status": "HOLD", "securityLevel": 1}
    if reason:
        out["reason"] = reason
    return out


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
        data = {"upstream_status": r.status_code}
    if r.is_success:
        return data
    raise HTTPException(status_code=r.status_code, detail=data)


@app.post("/gateway")
async def mandatory_gateway(payload: GatewayPayload):
    canonical_text, c_err = await canonical_loader()
    if c_err or not canonical_text:
        return _hold(reason=c_err or "canonical_error")

    inventory_text, i_err = await inventory_loader()
    if i_err or not inventory_text:
        return _hold(reason=i_err or "inventory_error")

    audit_blob = canonical_text + "\n\n---\n\n" + inventory_text
    if security_level_hold(audit_blob):
        return _hold(reason="inventory_state_hold_or_invalid")

    enforced_prompt = (
        f"### SYSTEM_CANONICAL_LAW ###\n{canonical_text}\n\n"
        f"### SYSTEM_INVENTORY ###\n{inventory_text}\n\n"
        f"### USER_REQUEST ###\n{payload.prompt}"
    )

    return await forward_to_ai_router(enforced_prompt, payload)


@app.get("/health")
def health():
    return {"status": "ok", "protocol": "NEXTBASE_API_GATEWAY_FIXED"}
