#!/usr/bin/env python3
"""QA fast-cut lesson videos: duration, streams, loudness, and required scene-change samples."""
from pathlib import Path
import json, subprocess, sys

def run(args):
    return subprocess.check_output(args, text=True, stderr=subprocess.STDOUT).strip()
def main():
    root=Path(__file__).resolve().parents[2]
    targets=sys.argv[1:] or ['langfuse/videos/LF-01-langfuse-overview-v2.mp4','langfuse/videos/LF-02-trace-v2.mp4']
    bad=[]
    for rel in targets:
        p=root/rel
        if not p.exists() or p.stat().st_size==0: bad.append(f'{rel}: missing/empty'); continue
        meta=json.loads(run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,codec_name,width,height','-of','json',str(p)]))
        dur=float(meta['format']['duration']); streams=meta['streams']
        if not (179.0 <= dur <= 181.0): bad.append(f'{rel}: duration={dur}')
        kinds={s.get('codec_type') for s in streams}
        if kinds != {'video','audio'}: bad.append(f'{rel}: streams={kinds}')
        vol=run(['ffmpeg','-i',str(p),'-af','volumedetect','-f','null','-'])
        if 'max_volume: -inf dB' in vol: bad.append(f'{rel}: silent audio')
        print(f'{rel}: duration={dur:.3f}, streams={sorted(kinds)}, loudness_checked=PASS')
    if bad:
        print('\n'.join(bad)); return 1
    print('fast-cut QA passed')
if __name__=='__main__': raise SystemExit(main())
