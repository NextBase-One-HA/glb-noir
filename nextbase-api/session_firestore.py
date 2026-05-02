"""
Session memory for nextbase-api /gateway.

AI memory is not trusted. Gateway loads externally persisted session state
from Firestore and injects it before forwarding to ai-router.
No state is stored on ai-router.
"""
from __future__ import annotations

import asyncio
import os
from datetime import datetime, timezone
from typing import Any

from google.cloud import firestore

_fs: firestore.Client | None = None

COL_SESSIONS = "sessions"
MAX_MESSAGES = int(os.getenv("NEXTBASE_SESSION_MAX_MESSAGES", "24"))
MAX_FIELD_CHARS = int(os.getenv("NEXTBASE_SESSION_MAX_FIELD_CHARS", "4000"))


def _client() -> firestore.Client:
    global _fs
    if _fs is None:
        project = (
            os.getenv("GOOGLE_CLOUD_PROJECT")
            or os.getenv("GCP_PROJECT")
            or os.getenv("GCLOUD_PROJECT")
            or None
        )
        _fs = firestore.Client(project=project) if project else firestore.Client()
    return _fs


def _utc_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_text(value: Any, limit: int = MAX_FIELD_CHARS) -> str:
    text = str(value or "")
    if len(text) <= limit:
        return text
    return text[:limit] + "...[truncated]"


def normalize_session_id(raw: str | None) -> str:
    text = "".join(c for c in (raw or "") if c.isalnum() or c in "-_")
    return text[:96]


async def session_context(
    *,
    session_id: str,
    canonical_snapshot: str,
    inventory_snapshot: str,
) -> str:
    """Return persisted session context and ensure the session doc exists."""
    sid = normalize_session_id(session_id)
    if not sid:
        return ""

    fs = _client()
    ref = fs.collection(COL_SESSIONS).document(sid)

    def read_or_create() -> dict[str, Any]:
        snap = ref.get()
        now = firestore.SERVER_TIMESTAMP
        if not snap.exists:
            ref.set(
                {
                    "session_id": sid,
                    "canonical_snapshot": _safe_text(canonical_snapshot),
                    "inventory_snapshot": _safe_text(inventory_snapshot),
                    "messages": [],
                    "created_at": now,
                    "last_updated": now,
                }
            )
            return {"messages": []}
        data = snap.to_dict() or {}
        ref.update(
            {
                "canonical_snapshot": _safe_text(canonical_snapshot),
                "inventory_snapshot": _safe_text(inventory_snapshot),
                "last_updated": now,
            }
        )
        return data

    data = await asyncio.to_thread(read_or_create)
    messages = data.get("messages") or []
    if not isinstance(messages, list):
        messages = []
    recent = messages[-MAX_MESSAGES:]
    if not recent:
        return "No prior session messages."

    lines: list[str] = []
    for idx, msg in enumerate(recent, start=1):
        if not isinstance(msg, dict):
            continue
        role = _safe_text(msg.get("role"), 32) or "unknown"
        content = _safe_text(msg.get("content"), 1200)
        ts = _safe_text(msg.get("ts"), 64)
        lines.append(f"{idx}. [{ts}] {role}: {content}")
    return "\n".join(lines) if lines else "No prior session messages."


async def session_record_exchange(
    *,
    session_id: str,
    user_prompt: str,
    assistant_response: Any,
) -> None:
    """Append the latest exchange to the session doc."""
    sid = normalize_session_id(session_id)
    if not sid:
        return

    fs = _client()
    ref = fs.collection(COL_SESSIONS).document(sid)
    now_iso = _utc_iso()

    def write() -> None:
        snap = ref.get()
        data = snap.to_dict() if snap.exists else {}
        messages = data.get("messages") if isinstance(data, dict) else []
        if not isinstance(messages, list):
            messages = []
        messages.extend(
            [
                {"role": "user", "content": _safe_text(user_prompt), "ts": now_iso},
                {"role": "assistant", "content": _safe_text(assistant_response), "ts": now_iso},
            ]
        )
        messages = messages[-MAX_MESSAGES:]
        ref.set(
            {
                "session_id": sid,
                "messages": messages,
                "last_updated": firestore.SERVER_TIMESTAMP,
            },
            merge=True,
        )

    await asyncio.to_thread(write)


async def session_status(*, session_id: str) -> dict[str, Any]:
    sid = normalize_session_id(session_id)
    if not sid:
        return {"exists": False, "error": "invalid_session_id"}
    fs = _client()
    ref = fs.collection(COL_SESSIONS).document(sid)

    def read() -> Any:
        return ref.get()

    snap = await asyncio.to_thread(read)
    if not snap.exists:
        return {"exists": False, "session_id": sid}
    data = snap.to_dict() or {}
    messages = data.get("messages") or []
    return {
        "exists": True,
        "session_id": sid,
        "message_count": len(messages) if isinstance(messages, list) else 0,
        "last_updated": str(data.get("last_updated")),
    }
