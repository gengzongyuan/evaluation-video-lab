#!/usr/bin/env python3
"""Validate Langfuse lesson manifest paths without exposing credentials."""
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
manifest_path = ROOT / "langfuse" / "manifest.json"
data = json.loads(manifest_path.read_text())
errors = []
for ep in data.get("episodes", []):
    for key in ("script", "source_verification", "recording_checklist", "evidence"):
        value = ep.get(key)
        if value and not (ROOT / value).exists():
            errors.append(f"{ep.get('id')}: missing {key}={value}")
    video = ep.get("video")
    if video and not (ROOT / video).exists():
        errors.append(f"{ep.get('id')}: missing video={video}")
    if ep.get("claim_level") not in {"L0", "L1", "L2", "L3"}:
        errors.append(f"{ep.get('id')}: invalid claim_level={ep.get('claim_level')}")
print(f"episodes={len(data.get('episodes', []))}")
if errors:
    print("manifest validation failed:")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)
print("manifest validation passed")
