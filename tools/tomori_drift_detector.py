#!/usr/bin/env python3
"""
Tomori Drift Detector

External drift detector for NextBase work.
The AI must not self-detect drift from memory.
This script reads the two canonical files first, then evaluates a response or task text.

Required canonical inputs:
- canonical/NEXTBASE_IMMUTABLE_CANONICAL.md
- canonical/NEXTBASE_DYNAMIC_CANONICAL.md

Usage:
  python3 tools/tomori_drift_detector.py response.txt
  printf '%s' "..." | python3 tools/tomori_drift_detector.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMMUTABLE = ROOT / "canonical" / "NEXTBASE_IMMUTABLE_CANONICAL.md"
DYNAMIC = ROOT / "canonical" / "NEXTBASE_DYNAMIC_CANONICAL.md"

REQUIRED_CANONICAL_TERMS = [
    "NextBase",
    "GLB",
    "Smile Friend Engine",
    "STELLA",
    "translate",
    "AI Router",
    "Self Optimization Layer",
    "Proof Mode",
]

REQUIRED_REPORT_SECTIONS = [
    "STATE:",
    "GOAL:",
    "BLOCKER:",
    "NEXT_ACTION:",
    "EVIDENCE:",
    "IRREVERSIBLE:",
    "OUTPUT:",
]

STOP_WORDS = ["ズレ", "違う", "ダメ", "HOLD", "rollback", "やめろ", "止まれ"]
OLD_WORKING_NAMES = ["NE Gateway"]
DECISION_WORDS = ["GO", "HOLD", "STOP", "PASS", "FAIL"]


def stop(reason: str) -> None:
    print(f"DRIFT_STOP: {reason}")
    sys.exit(1)


def read_text(path: Path) -> str:
    if not path.exists():
        stop(f"missing canonical file: {path}")
    data = path.read_text(encoding="utf-8")
    if not data.strip():
        stop(f"empty canonical file: {path}")
    return data


def read_input() -> str:
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).read_text(encoding="utf-8")
    return sys.stdin.read()


def main() -> None:
    immutable = read_text(IMMUTABLE)
    dynamic = read_text(DYNAMIC)
    canonical_joined = immutable + "\n" + dynamic

    missing_terms = [term for term in REQUIRED_CANONICAL_TERMS if term not in canonical_joined]
    if missing_terms:
        stop("canonical missing required terms: " + ", ".join(missing_terms))

    text = read_input()
    if not text.strip():
        stop("empty target text")

    # If the work mentions implementation/reporting, require structured output.
    if any(key in text for key in ["実行", "報告", "deploy", "curl", "Cloud Run", "修正"]):
        missing_sections = [s for s in REQUIRED_REPORT_SECTIONS if s not in text]
        if missing_sections:
            stop("target text missing report sections: " + ", ".join(missing_sections))

    if not any(word in text for word in DECISION_WORDS):
        stop("missing decision word GO/HOLD/STOP/PASS/FAIL")

    for old in OLD_WORKING_NAMES:
        if old in text and "historical" not in text and "旧" not in text and "AI Router" not in text:
            stop(f"old working name used without canonical mapping: {old}")

    # Stop words are allowed only if the text explicitly moves to HOLD or STOP.
    if any(w in text for w in STOP_WORDS) and not ("HOLD" in text or "STOP" in text):
        stop("stop word found without HOLD/STOP")

    print("DRIFT_DETECTOR_OK")


if __name__ == "__main__":
    main()
