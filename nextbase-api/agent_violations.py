"""Read recent agent DONE-rule violations from Firestore."""
from __future__ import annotations

import asyncio
import os
from typing import Any

from google.cloud import firestore

_fs: firestore.Client | None = None
COL_AGENT_VIOLATIONS = "agent_violations"


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


def _safe(value: Any, limit: int = 2000) -> str:
    text = str(value or "")
    return text if len(text) <= limit else text[:limit] + "...[truncated]"


async def recent_violations(limit: int = 10) -> dict[str, Any]:
    fs = _client()

    def read() -> list[dict[str, Any]]:
        query = (
            fs.collection(COL_AGENT_VIOLATIONS)
            .order_by("created_at", direction=firestore.Query.DESCENDING)
            .limit(limit)
        )
        rows: list[dict[str, Any]] = []
        for snap in query.stream():
            data = snap.to_dict() or {}
            rows.append(
                {
                    "violation_id": snap.id,
                    "event": data.get("event"),
                    "session_id": data.get("session_id"),
                    "blocking_tasks": data.get("blocking_tasks") or [],
                    "response_excerpt": _safe(data.get("response_excerpt")),
                    "created_at": str(data.get("created_at")),
                }
            )
        return rows

    return {"violations": await asyncio.to_thread(read)}
