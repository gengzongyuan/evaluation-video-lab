#!/usr/bin/env bash
set -euo pipefail

base_url="${LANGFUSE_BASE_URL:-${LANGFUSE_HOST:-}}"
if [[ -z "$base_url" ]]; then
  echo 'LANGFUSE_BASE_URL=missing'
  exit 2
fi
for name in LANGFUSE_PUBLIC_KEY LANGFUSE_SECRET_KEY; do
  if [[ -n "${!name:-}" ]]; then echo "$name=set"; else echo "$name=missing"; exit 2; fi
done
health="$(curl -fsS --max-time 8 "$base_url/api/public/health?failIfDatabaseUnavailable=true")"
printf '%s\n' "$health" | python3 -c 'import json,sys; d=json.load(sys.stdin); print("health_status="+str(d.get("status"))); print("server_version="+str(d.get("version"))); raise SystemExit(0 if d.get("status")=="OK" else 3)'
