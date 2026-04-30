#!/usr/bin/env python3
"""
Tomori Response Gate

Physical external correction layer for NextBase work.
This script checks whether a response/report follows the required zero-trust format.
It does not decide business truth. It only blocks unsafe reporting shape.

Usage:
  python3 tools/tomori_response_gate.py response.txt
  printf '%s' "...response..." | python3 tools/tomori_response_gate.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    "STATE:",
    "GOAL:",
    "BLOCKER:",
    "NEXT_ACTION:",
    "EVIDENCE:",
    "IRREVERSIBLE:",
    "OUTPUT:",
]

CANONICAL_NAMES = [
    "GLB",
    "Smile Friend Engine",
    "AI Router",
]

FORBIDDEN_NAMES = [
    "NE Gateway",
    "nextbase gateway as product",
]

RISKY_DONE_PATTERNS = [
    r"\bdone\b(?!.*\b(curl|log|test|evidence|HTTP|429|200)\b)",
    r"\bcomplete\b(?!.*\b(curl|log|test|evidence|HTTP|429|200)\b)",
    r"完了(?!.*(curl|ログ|テスト|証拠|HTTP|429|200))",
    r"OK(?!.*(curl|ログ|テスト|証拠|HTTP|429|200))",
]

RISKY_ASSERTIONS = [
    "たぶん",
    "おそらく",
    "多分",
    "可能性が高い",
    "ほぼ確定",
]

REQUIRED_DECISION_WORDS = ["HOLD", "GO", "PASS", "FAIL", "STOP"]


def read_input() -> str:
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).read_text(encoding="utf-8")
    return sys.stdin.read()


def fail(reason: str) -> None:
    print(f"STOP: {reason}")
    sys.exit(1)


def main() -> None:
    text = read_input()
    if not text.strip():
        fail("empty response")

    missing = [section for section in REQUIRED_SECTIONS if section not in text]
    if missing:
        fail("missing required sections: " + ", ".join(missing))

    if "EVIDENCE:" in text:
        evidence_part = text.split("EVIDENCE:", 1)[1]
        evidence_part = evidence_part.split("IRREVERSIBLE:", 1)[0]
        if not evidence_part.strip():
            fail("EVIDENCE section is empty")

    if not any(word in text for word in REQUIRED_DECISION_WORDS):
        fail("missing GO/HOLD/PASS/FAIL/STOP decision word")

    for bad in FORBIDDEN_NAMES:
        if bad in text:
            fail(f"forbidden name found: {bad}")

    # If old gateway service name is mentioned, require the canonical name nearby.
    if "nextbase-gateway-v1" in text and "AI Router" not in text:
        fail("nextbase-gateway-v1 mentioned without canonical name AI Router")

    for pattern in RISKY_DONE_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL):
            fail("completion claim without evidence marker")

    # Risky words are allowed only when explicitly marked as unconfirmed.
    for word in RISKY_ASSERTIONS:
        if word in text and "未確認" not in text and "HOLD" not in text:
            fail(f"risky assertion without HOLD/未確認: {word}")

    print("RESPONSE_GATE_OK")


if __name__ == "__main__":
    main()
