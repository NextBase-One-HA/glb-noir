import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools.glb_startup_integrity_gate import verify_gate


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class StartupIntegrityGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "App" / "Resources").mkdir(parents=True, exist_ok=True)
        (self.root / "security" / "layer_lock").mkdir(parents=True, exist_ok=True)

        immutable = self.root / "security" / "layer_lock" / "immutable_canonical_2026-04-22.json"
        dynamic = self.root / "security" / "layer_lock" / "NEXTBASE_DYNAMIC_CANONICAL_STATE.json"
        canonical_manifest = self.root / "security" / "layer_lock" / "canonical_manifest.json"
        layer_manifest = self.root / "App" / "Resources" / "layer_lock_manifest.json"
        startup_manifest = self.root / "App" / "Resources" / "startup_hash_manifest.json"

        immutable.write_text('{"x":1}\n', encoding="utf-8")
        dynamic.write_text('{"y":2}\n', encoding="utf-8")
        canonical_manifest.write_text('{"hashes":{}}\n', encoding="utf-8")
        layer_manifest.write_text(
            json.dumps(
                {
                    "entity_id": "NEXTBASE_LAYER_LOCK",
                    "root_key_id": "K0-REFERENCE-ONLY",
                    "signing_key_id": "K1-PROOF",
                    "profile_key_id": "K2-PROOF",
                    "revoke": {"status": "active"},
                },
                ensure_ascii=False,
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )

        startup_payload = {
            "build_id": "test-build",
            "hashes": {
                "immutable_json_file_sha256": _sha(immutable),
                "dynamic_json_file_sha256": _sha(dynamic),
                "canonical_manifest_file_sha256": _sha(canonical_manifest),
            },
            "approval": {
                "approval_mode": "GO",
                "signer_id": "NORI",
                "token_id": "TOKEN-1",
                "signature_status": "OK",
            },
        }
        startup_manifest.write_text(json.dumps(startup_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_permit_when_hash_and_approval_match(self) -> None:
        report = verify_gate(
            layer_root=self.root,
            app_version="test",
            release_channel="test",
            auth_path=self.root / "missing.json",
            skip_preflight=True,
            skip_revocation=True,
        )
        self.assertEqual(report["verification_status"], "PASS")
        self.assertEqual(report["reason_code"], "STARTUP_OK")

    def test_reject_on_immutable_mismatch(self) -> None:
        immutable = self.root / "security" / "layer_lock" / "immutable_canonical_2026-04-22.json"
        immutable.write_text('{"x":9}\n', encoding="utf-8")
        report = verify_gate(
            layer_root=self.root,
            app_version="test",
            release_channel="test",
            auth_path=self.root / "missing.json",
            skip_preflight=True,
            skip_revocation=True,
        )
        self.assertEqual(report["verification_status"], "FAIL")
        self.assertEqual(report["reason_code"], "IMMUTABLE_HASH_MISMATCH")

    def test_reject_on_dynamic_mismatch(self) -> None:
        dynamic = self.root / "security" / "layer_lock" / "NEXTBASE_DYNAMIC_CANONICAL_STATE.json"
        dynamic.write_text('{"y":9}\n', encoding="utf-8")
        report = verify_gate(
            layer_root=self.root,
            app_version="test",
            release_channel="test",
            auth_path=self.root / "missing.json",
            skip_preflight=True,
            skip_revocation=True,
        )
        self.assertEqual(report["verification_status"], "FAIL")
        self.assertEqual(report["reason_code"], "DYNAMIC_HASH_MISMATCH")

    def test_reject_when_approval_not_go(self) -> None:
        startup_manifest = self.root / "App" / "Resources" / "startup_hash_manifest.json"
        startup = json.loads(startup_manifest.read_text(encoding="utf-8"))
        startup["approval"]["approval_mode"] = "HOLD"
        startup_manifest.write_text(json.dumps(startup, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        report = verify_gate(
            layer_root=self.root,
            app_version="test",
            release_channel="test",
            auth_path=self.root / "missing.json",
            skip_preflight=True,
            skip_revocation=True,
        )
        self.assertEqual(report["verification_status"], "FAIL")
        self.assertEqual(report["reason_code"], "APPROVAL_MODE_INVALID")

    def test_reject_when_revoked(self) -> None:
        layer_manifest = self.root / "App" / "Resources" / "layer_lock_manifest.json"
        payload = json.loads(layer_manifest.read_text(encoding="utf-8"))
        payload["revoke"]["status"] = "revoked"
        layer_manifest.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        report = verify_gate(
            layer_root=self.root,
            app_version="test",
            release_channel="test",
            auth_path=self.root / "missing.json",
            skip_preflight=True,
            skip_revocation=True,
        )
        self.assertEqual(report["verification_status"], "FAIL")
        self.assertEqual(report["reason_code"], "REVOCATION_BLOCKED")


if __name__ == "__main__":
    unittest.main()
