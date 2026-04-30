#!/bin/bash
set -euo pipefail

BASE="${AI_ROUTER_BASE:-https://nextbase-gateway-v1-125142687526.asia-northeast1.run.app}"
OUT="${1:-/tmp/ai_router_probe_result.txt}"

: > "$OUT"

echo "STATE: PROBING_AI_ROUTER" | tee -a "$OUT"
echo "BASE: $BASE" | tee -a "$OUT"
echo "TIME_UTC: $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$OUT"
echo "" | tee -a "$OUT"

probe_get() {
  local path="$1"
  echo "---- GET $path ----" | tee -a "$OUT"
  curl -s -i "$BASE$path" | head -n 40 | tee -a "$OUT"
  echo "" | tee -a "$OUT"
}

probe_post() {
  local path="$1"
  echo "---- POST $path ----" | tee -a "$OUT"
  curl -s -i -X POST "$BASE$path" \
    -H "Content-Type: application/json" \
    -d '{"text":"hello","caller_id":"prod"}' | head -n 60 | tee -a "$OUT"
  echo "" | tee -a "$OUT"
}

probe_get "/health"
probe_get "/docs"
probe_post "/gateway"
probe_post "/translate"
probe_post "/"

if grep -q "HTTP/2 200" "$OUT" || grep -q "HTTP/1.1 200" "$OUT"; then
  echo "PROBE_RESULT: PASS_CANDIDATE_REVIEW_REQUIRED" | tee -a "$OUT"
  exit 0
fi

echo "PROBE_RESULT: HOLD_NO_200_ENDPOINT" | tee -a "$OUT"
exit 1
