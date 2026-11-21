#!/usr/bin/env python3
"""Quality gate for short-video prototypes.

Checks duration, portrait dimensions, H.264/AAC streams, non-silent audio,
subtitle presence, and visual change at representative timestamps.
"""
from __future__ import annotations
import argparse, hashlib, json, shutil, subprocess, sys, tempfile
from pathlib import Path

def run(cmd: list[str], check=True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, text=True, capture_output=True, check=check)

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("video", type=Path)
    ap.add_argument("--subtitle", action="append", type=Path, default=[])
    ap.add_argument("--tolerance", type=float, default=1.0)
    args = ap.parse_args()
    errors: list[str] = []
    if not args.video.is_file() or args.video.stat().st_size == 0:
        print(f"FAIL video missing/empty: {args.video}"); return 1
    probe = json.loads(run(["ffprobe","-v","error","-show_entries","format=duration:stream=index,codec_type,codec_name,width,height","-of","json",str(args.video)]).stdout)
    duration = float(probe.get("format",{}).get("duration",0))
    streams = probe.get("streams",[])
    video = next((s for s in streams if s.get("codec_type")=="video"), None)
    audio = next((s for s in streams if s.get("codec_type")=="audio"), None)
    if abs(duration-180)>args.tolerance: errors.append(f"duration={duration:.3f}, expected 180±{args.tolerance}")
    if not video: errors.append("missing video stream")
    else:
        if video.get("codec_name") != "h264": errors.append(f"video codec={video.get('codec_name')}, expected h264")
        if (video.get("width"),video.get("height")) != (1080,1920): errors.append(f"dimensions={video.get('width')}x{video.get('height')}, expected 1080x1920")
    if not audio: errors.append("missing audio stream")
    elif audio.get("codec_name") != "aac": errors.append(f"audio codec={audio.get('codec_name')}, expected aac")
    vol = run(["ffmpeg","-v","error","-i",str(args.video),"-af","volumedetect","-f","null","-"],check=False).stderr
    if "mean_volume: -inf" in vol or "max_volume: -inf" in vol:
        errors.append("audio is silent (mean/max volume -inf)")
    else:
        print("audio: non-silent")
    for sub in args.subtitle:
        if not sub.is_file() or sub.stat().st_size == 0: errors.append(f"subtitle missing/empty: {sub}")
    # Compare representative frame hashes; changes should occur between segments.
    times=[0,15,30,60,120,165]
    with tempfile.TemporaryDirectory(prefix="video-quality-") as td:
        hashes=[]
        for t in times:
            out=Path(td)/f"{t}.jpg"
            p=run(["ffmpeg","-y","-loglevel","error","-ss",str(t),"-i",str(args.video),"-frames:v","1","-update","1",str(out)],check=False)
            if p.returncode != 0 or not out.exists(): errors.append(f"frame extraction failed at {t}s"); continue
            hashes.append(hashlib.sha256(out.read_bytes()).hexdigest())
        if hashes and len(set(hashes)) < 3: errors.append(f"insufficient visual changes: {len(set(hashes))} unique frame hashes")
        print(f"frames: {len(set(hashes))}/{len(hashes)} unique at {times}")
    print(f"duration: {duration:.3f}s")
    print(f"streams: video={video.get('codec_name') if video else None}, audio={audio.get('codec_name') if audio else None}")
    for sub in args.subtitle: print(f"subtitle: {sub} {'OK' if sub.is_file() and sub.stat().st_size else 'MISSING'}")
    if errors:
        print("FAIL")
        for e in errors: print(f"- {e}")
        return 1
    print("PASS")
    return 0
if __name__ == "__main__": sys.exit(main())
