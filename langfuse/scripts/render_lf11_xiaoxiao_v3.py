#!/usr/bin/env python3
"""Render LF-11 same-dataset comparison with original-speed Xiaoxiao and burned captions."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "langfuse/build/lf11-xiaoxiao-v3"
BOARD = ROOT / "langfuse/LF-11-shot-board-xiaoxiao.md"
W, H = 1080, 1920
_spec = importlib.util.spec_from_file_location(
    "_lf02_render_primitives", ROOT / "langfuse/scripts/render_lf02_xiaoxiao_v3.py"
)
base = importlib.util.module_from_spec(_spec)
assert _spec.loader
_spec.loader.exec_module(base)
u = base.u
FFMPEG = base.FFMPEG

META = [
    ("01", "钩子", "平均分更高，也可能藏着关键回退", ["平均分", "关键失败"]),
    ("02", "同一 Dataset", "两个候选，先用同一组输入", ["固定输入"]),
    ("03", "item 对齐", "用稳定 item ID 对齐两条结果", ["错位打叉"]),
    ("04", "规则上锁", "同一评分规则，才有可比起点", ["空值", "失败"]),
    ("05", "基线与候选", "基线要先固定，不能事后挑", ["baseline", "candidate"]),
    ("06", "基线 run", "基线 run 留下逐条原始证据", ["item 输出"]),
    ("07", "候选 run", "比较谁，就只改变谁", ["只改一项"]),
    ("08", "成对对照", "先逐样本对照，再看汇总", ["item", "change"]),
    ("09", "回退聚光", "通过变失败的样本必须单独展开", ["回归"]),
    ("10", "缺口门", "缺失、失败、无评分都不能放行", ["missing", "failed"]),
    ("11", "空值处理", "空值按规则处理，不能偷偷改分母", ["unknown"]),
    ("12", "分群条", "分组结果必须带样本量", ["样本量留空"]),
    ("13", "重复运行", "一次差异，不等于稳定差异", ["波动"]),
    ("14", "成本延迟", "成本、延迟也要同条件、可回读", ["unknown", "P95"]),
    ("15", "元数据", "两次 run 的版和条件都要留下", ["脱敏 commit"]),
    ("16", "回读闭环", "按同一 run、item 回读结果", ["四步"]),
    ("17", "有界结论", "结论只适用于本次数据和条件", ["三层边界"]),
    ("18", "统计门", "观察到差异 ≠ 统计显著", ["两道门"]),
    ("19", "本集边界", "不是实验比较已完成", ["prototype / L1"]),
    ("20", "下一集", "从异常 Trace 到修复和回归", ["LF-12"]),
]
PALETTES = [
    ((13, 20, 38), (89, 155, 255), (237, 244, 255)),
    ((29, 17, 30), (255, 141, 164), (255, 237, 245)),
    ((13, 29, 26), (75, 219, 169), (230, 255, 246)),
    ((30, 22, 13), (255, 192, 89), (255, 246, 227)),
    ((17, 21, 42), (166, 146, 255), (239, 237, 255)),
    ((27, 17, 19), (255, 114, 114), (255, 237, 239)),
]


def load_shots():
    pattern = re.compile(r"^\| (\d{2}) \| `([^`]+)` \| [^|]+ \| (.*?) \| (.*?) \| (.*?) \|$", re.M)
    rows = {}
    for match in pattern.finditer(BOARD.read_text(encoding="utf-8")):
        sid, layout, voice, _visual, caption = match.groups()
        rows[sid] = dict(id=sid, layout=layout, voice=voice, caption=caption)
    shots = []
    for sid, kicker, title, chips in META:
        shot = rows[sid]
        shot.update(kicker=kicker, title=title, chips=chips)
        shots.append(shot)
    if len(shots) != 20 or len({s["layout"] for s in shots}) != 20:
        raise ValueError("expected 20 unique layouts")
    return shots


SHOTS = load_shots()


def label(draw, text, xy, size=32, color=(237, 244, 255), light=False, max_w=880):
    return base.label(draw, text, xy, size, color, light, max_w)


def header(draw, shot, idx, accent, fg):
    draw.text((72, 62), f"LF-11  ·  {shot['kicker']}", font=u.font(28, True), fill=accent)
    y = label(draw, shot["title"], (72, 118), 48, fg, max_w=930)
    y = max(y, 210)
    draw.text((72, y + 6), f"{idx:02d} / 20    prototype / L1", font=u.font(24, True), fill=(185, 195, 215))
    bar_y = y + 48
    u.rounded(draw, (72, bar_y, 1008, bar_y + 10), 5, (41, 48, 65))
    u.rounded(draw, (72, bar_y, 72 + int(936 * idx / 20), bar_y + 10), 5, accent)


def node(draw, xy, text, accent, fg, width=260, height=140):
    base.node(draw, xy, text, accent, fg, width, height)


def draw_shot(shot, idx):
    bg, accent, fg = PALETTES[(idx - 1) % len(PALETTES)]
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    header(d, shot, idx, accent, fg)
    y = 380
    layout = shot["layout"]
    if layout == "hook":
        u.panel(d, (90, y + 20, 990, y + 280))
        label(d, "平均分 ↑", (150, y + 100), 64, accent)
        u.panel(d, (90, y + 360, 990, y + 680), (65, 18, 28))
        label(d, "关键样本", (150, y + 430), 44, fg)
        label(d, "通过 → 失败", (150, y + 540), 40, (255, 140, 150))
    elif layout == "shared-dataset":
        node(d, (240, y), "同一 Dataset", accent, fg, 600, 160)
        node(d, (90, y + 320), "候选 A", accent, fg, 400, 180)
        node(d, (590, y + 320), "候选 B", accent, fg, 400, 180)
        d.line((540, y + 160, 290, y + 320), fill=accent, width=4)
        d.line((540, y + 160, 790, y + 320), fill=accent, width=4)
        label(d, "输入固定，分流比较", (260, y + 560), 36, fg)
    elif layout == "item-ids":
        for i, side in enumerate(["A", "B"]):
            xx = 90 + i * 480
            u.panel(d, (xx, y + 40, xx + 430, y + 620))
            label(d, f"run {side}", (xx + 40, y + 80), 36, accent)
            for j in range(3):
                label(d, f"item_0{j+1}", (xx + 50, y + 200 + j * 110), 34, fg)
        d.line((520, y + 230, 560, y + 230), fill=accent, width=4)
        d.line((520, y + 340, 560, y + 340), fill=accent, width=4)
        d.line((500, y + 470, 580, y + 540), fill=(255, 140, 150), width=6)
        label(d, "错位连接打叉", (360, y + 680), 32, (255, 140, 150))
    elif layout == "rule-lock":
        u.panel(d, (90, y + 40, 990, y + 280))
        label(d, "评分规则 已上锁", (150, y + 120), 48, fg)
        node(d, (90, y + 360), "空值规则", accent, fg, 420, 220)
        node(d, (570, y + 360), "失败判定", accent, fg, 420, 220)
    elif layout == "baseline-candidate":
        u.panel(d, (70, y + 40, 500, y + 680))
        label(d, "baseline", (140, y + 140), 44, fg)
        label(d, "已审查，不可事后替换", (110, y + 360), 32, accent, max_w=350)
        u.panel(d, (580, y + 40, 1010, y + 680))
        label(d, "candidate", (640, y + 140), 44, fg)
        label(d, "待比较", (680, y + 360), 36, accent)
    elif layout == "run-a":
        u.panel(d, (90, y + 40, 990, y + 680))
        label(d, "基线 run 抽屉", (150, y + 80), 40, accent)
        for i, item in enumerate(["item 原始输出", "metadata", "运行时间"]):
            yy = y + 200 + i * 140
            label(d, item, (180, yy), 40, fg)
            label(d, "已保存", (720, yy + 8), 28, accent)
    elif layout == "run-b":
        for i, (name, state) in enumerate([("Prompt", "可改"), ("模型", "锁定"), ("参数", "锁定"), ("数据", "锁定")]):
            yy = y + i * 165
            u.panel(d, (90, yy, 990, yy + 140))
            label(d, name, (150, yy + 40), 40, fg)
            label(d, state, (700, yy + 48), 32, accent if state == "可改" else (180, 190, 210))
    elif layout == "pair-table":
        heads = ["item", "A", "B", "变化"]
        for c, h in enumerate(heads):
            label(d, h, (100 + c * 230, y + 20), 30, accent, True, 200)
        for r in range(4):
            for c in range(4):
                x, yy = 80 + c * 235, y + 100 + r * 140
                u.panel(d, (x, yy, x + 215, yy + 120))
                text = f"0{r+1}" if c == 0 else "示意"
                label(d, text, (x + 50, yy + 35), 30, fg)
    elif layout == "regression-spotlight":
        u.panel(d, (90, y + 20, 990, y + 220), (24, 30, 44))
        label(d, "平均分（背景）", (150, y + 90), 36, (160, 170, 190))
        u.panel(d, (90, y + 280, 990, y + 680), (65, 18, 28))
        label(d, "回归样本", (150, y + 360), 48, fg)
        label(d, "通过 → 失败", (150, y + 500), 40, (255, 140, 150))
    elif layout == "missing-gate":
        u.panel(d, (90, y + 40, 990, y + 220))
        label(d, "发布门前", (150, y + 100), 48, fg)
        for i, text in enumerate(["missing", "failed", "no score"]):
            node(d, (70 + i * 330, y + 320), text, (255, 140, 150), fg, 290, 220)
    elif layout == "null-handling":
        node(d, (240, y), "空值", accent, fg, 600, 150)
        node(d, (90, y + 280), "按规则处理", accent, fg, 900, 140)
        node(d, (90, y + 480), "算成零分 ×", (255, 140, 150), fg, 420, 150)
        node(d, (570, y + 480), "偷偷删分母 ×", (255, 140, 150), fg, 420, 150)
    elif layout == "cohort-bars":
        for i, name in enumerate(["场景 A", "场景 B", "场景 C"]):
            yy = y + 20 + i * 210
            label(d, name, (90, yy), 32, fg)
            u.rounded(d, (90, yy + 60, 720, yy + 120), 16, (25, 32, 48))
            u.rounded(d, (90, yy + 60, 90 + (220 + i * 90), yy + 120), 16, accent)
            label(d, "n 留空", (780, yy + 60), 28, accent)
    elif layout == "repeat-runs":
        d.line((120, y + 520, 960, y + 520), fill=(80, 90, 110), width=4)
        for i in range(8):
            x = 160 + i * 100
            yy = y + 280 + ((-1) ** i) * (40 + i * 8)
            d.ellipse((x - 16, yy - 16, x + 16, yy + 16), fill=accent if i % 2 else (255, 141, 164))
        label(d, "单次差异", (150, y + 80), 40, fg)
        label(d, "稳定区间未计算前留空", (150, y + 600), 36, accent)
    elif layout == "cost-latency":
        node(d, (90, y + 40), "cost", accent, fg, 420, 220)
        node(d, (570, y + 40), "latency", accent, fg, 420, 220)
        node(d, (90, y + 340), "unknown 保留", (255, 180, 120), fg, 420, 200)
        node(d, (570, y + 340), "P95 未证明", (255, 140, 150), fg, 420, 200)
        label(d, "同条件比较，不外推长期", (180, y + 600), 36, fg)
    elif layout == "metadata":
        items = ["Dataset 版本", "Prompt", "模型 / 参数", "SDK / 代码", "运行时间"]
        for i, item in enumerate(items):
            yy = y + i * 130
            u.panel(d, (90, yy, 990, yy + 110))
            label(d, item, (140, yy + 30), 34, fg)
            label(d, "A/B 对应", (720, yy + 34), 26, accent, True)
    elif layout == "readback-loop":
        for i, item in enumerate(["run A 回读", "run B 回读", "同一 item", "失败类型"]):
            yy = y + i * 175
            node(d, (140, yy), item, accent, fg, 800, 140)
            if i < 3:
                d.polygon([(520, yy + 148), (560, yy + 148), (540, yy + 175)], fill=accent)
    elif layout == "bounded-claim":
        u.panel(d, (80, y + 20, 1000, y + 700))
        u.panel(d, (130, y + 90, 950, y + 620))
        u.panel(d, (190, y + 180, 890, y + 520))
        label(d, "数据", (230, y + 50), 28, accent)
        label(d, "版本", (230, y + 120), 28, accent)
        label(d, "条件", (230, y + 210), 28, accent)
        label(d, "本次观察到…", (260, y + 320), 40, fg)
        label(d, "不是全面领先", (260, y + 410), 32, (255, 160, 170))
    elif layout == "stats-gate":
        u.panel(d, (90, y + 40, 990, y + 300))
        label(d, "观察到差异", (150, y + 130), 48, fg)
        u.panel(d, (90, y + 380, 990, y + 680), (50, 28, 18))
        label(d, "统计显著", (150, y + 460), 48, (255, 180, 120))
        label(d, "缺样本量 / 波动 / 区间就不说", (150, y + 560), 32, fg)
    elif layout == "stamp":
        u.panel(d, (72, y + 45, 1008, y + 710), (40, 17, 24))
        label(d, "PROTOTYPE", (135, y + 115), 68, (255, 140, 150))
        label(d, "L1 / 课程示意", (135, y + 250), 54, fg)
        for i, item in enumerate(["run A：未证明", "run B：未证明", "Score 回读：未证明"]):
            label(d, item, (135, y + 390 + i * 80), 34, (255, 170, 180))
    elif layout == "cta":
        u.panel(d, (72, y + 55, 1008, y + 720), tuple(int(c * .35) for c in accent))
        label(d, "下一集 / LF-12", (130, y + 115), 38, fg)
        label(d, "异常 Trace → 修复 → 回归", (130, y + 270), 44, accent)
        for i, text in enumerate(["定位", "修复", "回归"]):
            node(d, (120 + i * 300, y + 480), text, accent, fg, 260, 140)
    else:
        raise ValueError(f"unknown layout: {layout}")
    u.chips(d, shot["chips"], H - 360, accent, fg)
    u.caption_box(d, shot["caption"], accent, fg)
    return im


def main() -> int:
    for name in ["audio", "frames", "clips"]:
        (BUILD / name).mkdir(parents=True, exist_ok=True)
    timeline, clips, start = [], [], 0.0
    for idx, shot in enumerate(SHOTS, start=1):
        audio = BUILD / "audio" / f"{shot['id']}.mp3"
        if not audio.exists() or audio.stat().st_size < 1000:
            base.synth(shot["voice"], audio)
        seconds = base.duration(audio)
        png = BUILD / "frames" / f"{shot['id']}.png"
        draw_shot(shot, idx).save(png, "PNG")
        clip = BUILD / "clips" / f"{shot['id']}.mp4"
        base.encode_clip(png, audio, clip, seconds)
        timeline.append({"id": shot["id"], "layout": shot["layout"], "start": start,
                         "end": start + seconds, "caption": shot["caption"], "voice": shot["voice"]})
        clips.append(clip)
        start += seconds
        print(f"shot {shot['id']}: {seconds:.3f}s / {shot['layout']}", flush=True)
    concat = BUILD / "concat.txt"
    concat.write_text("".join(f"file '{p}'\n" for p in clips), encoding="utf-8")
    video = ROOT / "langfuse/videos/LF-11-compare-xiaoxiao-v3.mp4"
    base.run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
              "-i", str(concat), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
              "-b:a", "128k", "-movflags", "+faststart", str(video)])
    srt, vtt = [], ["WEBVTT", ""]
    for i, item in enumerate(timeline, start=1):
        srt += [str(i), f"{base.ts(item['start'], True)} --> {base.ts(item['end'], True)}", item["caption"], ""]
        vtt += [f"{base.ts(item['start'])} --> {base.ts(item['end'])}", item["caption"], ""]
    (ROOT / "langfuse/captions/LF-11-xiaoxiao-v3.srt").write_text("\n".join(srt), encoding="utf-8")
    (ROOT / "langfuse/captions/LF-11-xiaoxiao-v3.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (BUILD / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"video": str(video), "duration": base.duration(video), "shots": len(timeline),
                      "last_caption_end": timeline[-1]["end"]}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
