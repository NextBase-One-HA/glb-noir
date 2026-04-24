#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = ROOT / "logs"
AUDIT_LOG = LOG_DIR / "startup_integrity_audit.jsonl"
AUDIT_LATEST = LOG_DIR / "startup_integrity.latest.json"
GLB_MANIFEST = ROOT / "monitoring" / "glb_startup_manifest.latest.json"

DEFAULT_LAYER_ROOT = Path("/Users/user/nextbase_self_opt_layer")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")


def fail(reason_code: str, detail: str) -> tuple[bool, str, str]:
    return False, reason_code, detail


def verify_gate(
    *,
    layer_root: Path,
    app_version: str,
    release_channel: str,
    auth_path: Path,
    skip_preflight: bool,
    skip_revocation: bool,
) -> dict[str, Any]:
    startup_path = layer_root / "App" / "Resources" / "startup_hash_manifest.json"
    canonical_manifest_path = layer_root / "security" / "layer_lock" / "canonical_manifest.json"
    immutable_json_path = layer_root / "security" / "layer_lock" / "immutable_canonical_2026-04-22.json"
    dynamic_json_path = layer_root / "security" / "layer_lock" / "NEXTBASE_DYNAMIC_CANONICAL_STATE.json"
    layer_manifest_path = layer_root / "App" / "Resources" / "layer_lock_manifest.json"

    report: dict[str, Any] = {
        "timestamp": now_iso(),
        "event": "startup_integrity_gate",
        "verification_status": "FAIL",
        "reason_code": "UNKNOWN",
        "detail": "",
        "build_id": "",
        "app_version": app_version,
        "release_channel": release_channel,
        "manifest_sha256": "",
        "revocation_status": "UNKNOWN",
    }

    required_files = [
        startup_path,
        canonical_manifest_path,
        immutable_json_path,
        dynamic_json_path,
        layer_manifest_path,
    ]
    for file_path in required_files:
        if not file_path.exists():
            report["reason_code"] = "STARTUP_FILE_MISSING"
            report["detail"] = str(file_path)
            return report

    startup = load_json(startup_path)
    report["build_id"] = str(startup.get("build_id", ""))
    report["manifest_sha256"] = sha256_file(startup_path)

    hashes = startup.get("hashes", {})
    approval = startup.get("approval", {})
    if not isinstance(hashes, dict) or not isinstance(approval, dict):
        report["reason_code"] = "STARTUP_MANIFEST_SHAPE_INVALID"
        report["detail"] = "hashes/approval must be object"
        return report

    immutable_hash = str(hashes.get("immutable_json_file_sha256", ""))
    dynamic_hash = str(hashes.get("dynamic_json_file_sha256", ""))
    manifest_hash = str(hashes.get("canonical_manifest_file_sha256", ""))
    if not immutable_hash or not dynamic_hash or not manifest_hash:
        report["reason_code"] = "STARTUP_HASH_FIELD_MISSING"
        report["detail"] = "missing immutable/dynamic/manifest hash field"
        return report

    current_immutable = sha256_file(immutable_json_path)
    if current_immutable != immutable_hash:
        report["reason_code"] = "IMMUTABLE_HASH_MISMATCH"
        report["detail"] = f"{current_immutable} != {immutable_hash}"
        return report

    current_dynamic = sha256_file(dynamic_json_path)
    if current_dynamic != dynamic_hash:
        report["reason_code"] = "DYNAMIC_HASH_MISMATCH"
        report["detail"] = f"{current_dynamic} != {dynamic_hash}"
        return report

    current_manifest = sha256_file(canonical_manifest_path)
    if current_manifest != manifest_hash:
        report["reason_code"] = "MANIFEST_HASH_MISMATCH"
        report["detail"] = f"{current_manifest} != {manifest_hash}"
        return report

    approval_mode = str(approval.get("approval_mode", "")).upper()
    signer_id = str(approval.get("signer_id", "")).strip()
    token_id = str(approval.get("token_id", "")).strip()
    signature_status = str(approval.get("signature_status", "")).upper()
    if approval_mode != "GO":
        report["reason_code"] = "APPROVAL_MODE_INVALID"
        report["detail"] = f"approval_mode={approval_mode}"
        return report
    if not signer_id or not token_id:
        report["reason_code"] = "APPROVAL_ID_MISSING"
        report["detail"] = "signer_id/token_id missing"
        return report
    if signature_status not in {"OK", "VALID"}:
        report["reason_code"] = "APPROVAL_SIGNATURE_INVALID"
        report["detail"] = f"signature_status={signature_status}"
        return report

    layer_manifest = load_json(layer_manifest_path)
    revoke_status = "UNKNOWN"
    revoke = layer_manifest.get("revoke")
    if isinstance(revoke, dict) and "status" in revoke:
        revoke_status = str(revoke.get("status", "UNKNOWN")).upper()
        if revoke_status != "ACTIVE":
            report["revocation_status"] = revoke_status
            report["reason_code"] = "REVOCATION_BLOCKED"
            report["detail"] = f"revoke.status={revoke_status}"
            return report

    if not skip_preflight:
        proc = subprocess.run(
            [
                "python3",
                str(layer_root / "tools" / "security" / "preflight_gate.py"),
                "--auth",
                str(auth_path),
            ],
            cwd=str(layer_root),
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            report["reason_code"] = "PREFLIGHT_GATE_FAILED"
            report["detail"] = (proc.stdout + "\n" + proc.stderr).strip()
            return report

    if not skip_revocation:
        proc = subprocess.run(
            [
                "python3",
                str(layer_root / "tools" / "security" / "check_revocation.py"),
                "--entity-id",
                str(layer_manifest.get("entity_id", "")),
                "--key-id",
                str(layer_manifest.get("root_key_id", "")),
                "--key-id",
                str(layer_manifest.get("signing_key_id", "")),
                "--key-id",
                str(layer_manifest.get("profile_key_id", "")),
            ],
            cwd=str(layer_root),
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0:
            report["reason_code"] = "REVOCATION_CHECK_FAILED"
            report["detail"] = (proc.stdout + "\n" + proc.stderr).strip()
            report["revocation_status"] = "BLOCKED"
            return report
        revoke_status = "ACTIVE"
    elif revoke_status == "UNKNOWN":
        revoke_status = "SKIPPED"

    report["revocation_status"] = revoke_status

    report["verification_status"] = "PASS"
    report["reason_code"] = "STARTUP_OK"
    report["detail"] = "startup integrity checks passed"

    glb_manifest = {
        "schema": "nextbase.glb_startup_manifest.v1",
        "timestamp": report["timestamp"],
        "build_id": report["build_id"],
        "app_version": app_version,
        "immutable_json_sha256": immutable_hash,
        "dynamic_json_sha256": dynamic_hash,
        "manifest_sha256": report["manifest_sha256"],
        "approval_mode": approval_mode,
        "signer_id": signer_id,
        "token_id": token_id,
        "revocation_status": revoke_status,
        "release_channel": release_channel,
    }
    write_json(GLB_MANIFEST, glb_manifest)
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--layer-root", default=str(DEFAULT_LAYER_ROOT))
    parser.add_argument("--app-version", default="glb-unknown")
    parser.add_argument("--release-channel", default="glb_2_99")
    parser.add_argument("--auth", default="")
    parser.add_argument("--mode", choices=["check", "report"], default="check")
    parser.add_argument("--skip-preflight", action="store_true")
    parser.add_argument("--skip-revocation", action="store_true")
    args = parser.parse_args()

    layer_root = Path(args.layer_root).resolve()
    auth_path = Path(args.auth).resolve() if args.auth else (layer_root / "security" / "layer_lock" / "nori_approval.sample.json")
    report = verify_gate(
        layer_root=layer_root,
        app_version=args.app_version,
        release_channel=args.release_channel,
        auth_path=auth_path,
        skip_preflight=args.skip_preflight,
        skip_revocation=args.skip_revocation,
    )
    write_json(AUDIT_LATEST, report)
    append_jsonl(AUDIT_LOG, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.mode == "check" and report.get("verification_status") != "PASS":
        sys.exit(2)


if __name__ == "__main__":
    main()
