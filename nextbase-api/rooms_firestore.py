"""
Rooms / messages / audit_logs — Firestore is the only source of truth for TTL and room state.
No state is stored on ai-router.
"""
from __future__ import annotations

import asyncio
import os
import random
from datetime import datetime, timedelta, timezone
from typing import Any

from google.cloud import firestore

_fs: firestore.Client | None = None

COL_ROOMS = "rooms"
COL_MESSAGES = "messages"
COL_AUDIT = "audit_logs"


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


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def normalize_room_code(raw: str) -> str:
    digits = "".join(c for c in (raw or "") if c.isdigit())
    if not digits:
        return ""
    if len(digits) >= 6:
        return digits[:6]
    return digits.zfill(6)


def _gen_code() -> str:
    return f"{random.randint(0, 999999):06d}"


def _expires_valid(expires_at: Any) -> bool:
    if expires_at is None:
        return False
    if isinstance(expires_at, datetime):
        ex = expires_at if expires_at.tzinfo else expires_at.replace(tzinfo=timezone.utc)
        return ex > _utc_now()
    return True


async def _audit(event: str, room_id: str, detail: dict[str, Any] | None = None) -> None:
    fs = _client()

    def _write() -> None:
        fs.collection(COL_AUDIT).add(
            {
                "event": event,
                "room_id": room_id,
                "detail": detail or {},
                "created_at": firestore.SERVER_TIMESTAMP,
            }
        )

    await asyncio.to_thread(_write)


async def room_create(*, ttl_days: int = 30) -> dict[str, Any]:
    fs = _client()
    expires_dt = _utc_now() + timedelta(days=ttl_days)

    for _ in range(24):
        code = _gen_code()
        ref = fs.collection(COL_ROOMS).document(code)

        def try_create(
            r: Any = ref,
            c: str = code,
            exp: datetime = expires_dt,
            td: int = ttl_days,
        ) -> bool:
            snap = r.get()
            if snap.exists:
                return False
            r.set(
                {
                    "code": c,
                    "created_at": firestore.SERVER_TIMESTAMP,
                    "expires_at": exp,
                    "ttl_days": td,
                }
            )
            return True

        ok = await asyncio.to_thread(try_create)
        if not ok:
            continue

        await _audit("room_created", code, {"ttl_days": ttl_days})
        return {
            "room_id": code,
            "code": code,
            "expires_at": expires_dt.isoformat(),
            "ttl_days": ttl_days,
        }

    raise RuntimeError("room_code_collision")


async def room_get_snapshot(code: str) -> tuple[dict[str, Any] | None, str | None]:
    """Returns (data, error_code). error_code: not_found | expired | invalid_code."""
    norm = normalize_room_code(code)
    if len(norm) != 6:
        return None, "invalid_code"
    fs = _client()
    ref = fs.collection(COL_ROOMS).document(norm)

    def read() -> Any:
        return ref.get()

    snap = await asyncio.to_thread(read)
    if not snap.exists:
        return None, "not_found"
    data = snap.to_dict() or {}
    if not _expires_valid(data.get("expires_at")):
        return None, "expired"
    return data, None


async def room_join(*, code: str) -> dict[str, Any]:
    data, err = await room_get_snapshot(code)
    if err == "invalid_code":
        return {"ok": False, "error": "invalid_code"}
    if err == "not_found":
        return {"ok": False, "error": "not_found"}
    if err == "expired":
        return {"ok": False, "error": "expired"}
    assert data is not None
    rid = str(data.get("code") or normalize_room_code(code))
    ex = data.get("expires_at")
    if isinstance(ex, datetime):
        ex_iso = ex.isoformat()
    else:
        ex_iso = str(ex) if ex is not None else ""
    await _audit("room_join", rid, {})
    return {"ok": True, "room_id": rid, "code": rid, "expires_at": ex_iso}


async def room_message(*, room_code: str, body: str, sender_id: str | None) -> dict[str, Any]:
    data, err = await room_get_snapshot(room_code)
    if err == "invalid_code":
        return {"ok": False, "error": "invalid_code"}
    if err == "not_found":
        return {"ok": False, "error": "not_found"}
    if err == "expired":
        return {"ok": False, "error": "expired"}
    assert data is not None
    rid = str(data.get("code") or normalize_room_code(room_code))
    fs = _client()

    def write_msg() -> str:
        doc_ref = fs.collection(COL_MESSAGES).document()
        doc_ref.set(
            {
                "room_id": rid,
                "body": body,
                "sender_id": sender_id,
                "created_at": firestore.SERVER_TIMESTAMP,
            }
        )
        return doc_ref.id

    msg_id = await asyncio.to_thread(write_msg)
    await _audit(
        "message_posted",
        rid,
        {"message_id": msg_id, "sender_id": sender_id},
    )
    return {"ok": True, "room_id": rid, "message_id": msg_id}


async def room_status(*, code: str) -> dict[str, Any]:
    norm = normalize_room_code(code)
    if len(norm) != 6:
        return {"exists": False, "error": "invalid_code"}
    fs = _client()
    ref = fs.collection(COL_ROOMS).document(norm)

    def read() -> Any:
        return ref.get()

    snap = await asyncio.to_thread(read)
    if not snap.exists:
        return {"exists": False, "error": "not_found"}
    data = snap.to_dict() or {}
    ex = data.get("expires_at")
    if not isinstance(ex, datetime):
        return {"exists": True, "error": "bad_schema"}
    ex_utc = ex if ex.tzinfo else ex.replace(tzinfo=timezone.utc)
    remaining = (ex_utc - _utc_now()).total_seconds()
    expired = remaining <= 0
    return {
        "exists": True,
        "room_id": norm,
        "code": norm,
        "expires_at": ex_utc.isoformat(),
        "expired": expired,
        "seconds_remaining": max(0, int(remaining)),
    }
