#!/usr/bin/env python3
"""Natural-voice quality gate for Langfuse short videos.

This gate exists because check_video_quality.py and qa_fastcut_video.py will
PASS stretched TTS, mismatched SRT/VTT, and 12 static cards as long as an AAC
stream exists. It does not claim Langfuse runtime evidence.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

FFMPEG = "/opt/homebrew/opt/ffmpeg@7/bin/ffmpeg"
FFPROBE = "/opt/homebrew/opt/ffmpeg@7/bin/ffprobe"
REPLACEMENT = "\ufffd"
TS_RE = re.compile(
    r"(?P<h>\d{1,2}):(?P<m>\d{2}):(?P<s>\d{2})[\.,](?P<ms>\d{1,3})"
    r"|(?P<mm>\d{1,2}):(?P<ss>\d{2})[\.,](?P<mms>\d{1,3})"
)


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    exe = Path(cmd[0])
    if not exe.exists():
        cmd = [cmd[0].split("/")[-1], *cmd[1:]]
    return subprocess.run(cmd, text=True, capture_output=True)


def probe(path: Path) -> dict:
    p = run(
        [
            FFPROBE,
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=index,codec_type,codec_name,duration,width,height",
            "-of",
            "json",
            str(path),
        ]
    )
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip() or "ffprobe failed")
    return json.loads(p.stdout)


def parse_ts(token: str) -> float:
    m = TS_RE.fullmatch(token.strip())
    if not m:
        raise ValueError(f"bad timestamp: {token!r}")
    if m.group("h") is not None:
        h = int(m.group("h"))
        mm = int(m.group("m"))
        ss = int(m.group("s"))
        frac = m.group("ms").ljust(3, "0")[:3]
        return h * 3600 + mm * 60 + ss + int(frac) / 1000
    mm = int(m.group("mm"))
    ss = int(m.group("ss"))
    frac = m.group("mms").ljust(3, "0")[:3]
    return mm * 60 + ss + int(frac) / 1000


def cue_times(text: str) -> list[tuple[float, float]]:
    times = []
    for raw in text.splitlines():
        line = raw.strip()
        if "-->" not in line:
            continue
        left, right = [part.strip().split()[0] for part in line.split("-->", 1)]
        times.append((parse_ts(left), parse_ts(right)))
    return times


def last_end(text: str) -> float:
    cues = cue_times(text)
    if not cues:
        raise ValueError("no cues")
    return max(end for _, end in cues)


def mistaken_15_min(text: str) -> list[str]:
    bad = []
    for raw in text.splitlines():
        if "-->" not in raw:
            continue
        for token in raw.replace(",", ".").split():
            m = re.fullmatch(r"(\d{2}):(\d{2}):(\d{2})\.\d+", token)
            if m and int(m.group(1)) == 0 and int(m.group(2)) >= 15:
                # 00:15:00 in a ~3 min video is the known 15-minute typo.
                if int(m.group(2)) >= 15:
                    bad.append(raw.strip())
                    break
    return bad


def trailing_silence_to_eof(video: Path, duration: float) -> float:
    p = run(
        [
            FFMPEG,
            "-hide_banner",
            "-i",
            str(video),
            "-af",
            "silencedetect=noise=-35dB:d=0.8",
            "-f",
            "null",
            "-",
        ]
    )
    starts, ends = [], []
    for line in (p.stderr or "").splitlines():
        if "silence_start:" in line:
            try:
                starts.append(float(line.split("silence_start:")[1].split()[0]))
            except ValueError:
                pass
        if "silence_end:" in line:
            try:
                ends.append(float(line.split("silence_end:")[1].split()[0]))
            except ValueError:
                pass
    if not starts:
        return 0.0
    last_start = starts[-1]
    if len(ends) < len(starts):
        return max(0.0, duration - last_start)
    last_end_t = ends[-1]
    # Silence that ends within 0.25s of EOF still counts as trailing.
    if duration - last_end_t <= 0.25:
        return max(0.0, last_end_t - last_start)
    if duration - last_start <= 1.5:
        return max(0.0, duration - last_start)
    return 0.0


def load_shot_ids(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        if "shots" in data:
            data = data["shots"]
        elif "timeline" in data:
            data = data["timeline"]
    if not isinstance(data, list):
        raise ValueError("shots JSON must be a list or contain shots/timeline")
    ids = []
    for item in data:
        if isinstance(item, dict):
            sid = item.get("id") or item.get("shot_id") or item.get("name")
            if sid is None:
                raise ValueError("shot object missing id")
            ids.append(str(sid))
        else:
            ids.append(str(item))
    return ids


def main() -> int:
    ap = argparse.ArgumentParser(description="Fail stretched TTS, caption drift, and trailing silence.")
    ap.add_argument("video", type=Path)
    ap.add_argument("--subtitle", action="append", type=Path, default=[], required=False)
    ap.add_argument("--shots", type=Path, help="timeline/shots JSON with unique shot ids")
    args = ap.parse_args()
    errors: list[str] = []
    notes: list[str] = []

    if not args.video.is_file() or args.video.stat().st_size == 0:
        print(f"FAIL video missing/empty: {args.video}")
        return 1

    meta = probe(args.video)
    fmt_dur = float(meta.get("format", {}).get("duration") or 0)
    streams = meta.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    if not video:
        errors.append("missing video stream")
    if not audio:
        errors.append("missing audio stream")
    else:
        audio_dur = float(audio.get("duration") or fmt_dur)
        delta = abs(fmt_dur - audio_dur)
        print(f"duration: format={fmt_dur:.3f}s audio={audio_dur:.3f}s delta={delta:.3f}s")
        if delta > 0.35:
            errors.append(f"video/audio duration delta {delta:.3f}s > 0.35s")

    trail = trailing_silence_to_eof(args.video, fmt_dur) if fmt_dur else 0.0
    print(f"trailing_silence: {trail:.3f}s")
    if trail > 1.5:
        errors.append(f"trailing silence after last speech {trail:.3f}s > 1.5s")

    if len(args.subtitle) < 2:
        errors.append("need both SRT and VTT via repeated --subtitle")
    srt = vtt = None
    for sub in args.subtitle:
        if not sub.is_file() or sub.stat().st_size == 0:
            errors.append(f"subtitle missing/empty: {sub}")
            continue
        text = sub.read_text(encoding="utf-8")
        if REPLACEMENT in text:
            errors.append(f"replacement char in {sub}")
        if "15:00" in text or mistaken_15_min(text):
            errors.append(f"mistaken 15:00-style timestamp in {sub}")
        try:
            end = last_end(text)
        except ValueError as exc:
            errors.append(f"{sub}: {exc}")
            continue
        print(f"subtitle {sub.name}: last_end={end:.3f}s gap_to_video={fmt_dur-end:.3f}s")
        if fmt_dur - end > 0.40:
            errors.append(f"{sub.name} ends {fmt_dur-end:.3f}s before video end")
        if sub.suffix.lower() == ".srt":
            srt = end
        elif sub.suffix.lower() == ".vtt":
            vtt = end
    if srt is not None and vtt is not None:
        cue_delta = abs(srt - vtt)
        print(f"srt_vtt_last_delta: {cue_delta:.3f}s")
        if cue_delta > 0.08:
            errors.append(f"SRT/VTT last timestamp delta {cue_delta:.3f}s > 80ms")

    if args.shots:
        if not args.shots.is_file():
            errors.append(f"shots file missing: {args.shots}")
        else:
            try:
                ids = load_shot_ids(args.shots)
            except ValueError as exc:
                errors.append(f"shots JSON: {exc}")
            else:
                unique = len(set(ids))
                print(f"shots: {unique} unique / {len(ids)} listed")
                if unique < 18:
                    errors.append(f"unique shot ids {unique} < 18")
    else:
        notes.append(
            "SHOTS_SKIP: ffmpeg scene>=18 is unreliable on dark-themed cards; pass --shots timeline.json with >=18 unique ids"
        )
        print(notes[-1])

    if errors:
        print("FAIL")
        for e in errors:
            print(f"- {e}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
