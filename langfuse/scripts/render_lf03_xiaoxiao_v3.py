#!/usr/bin/env python3
"""Render LF-03 with original-speed Xiaoxiao TTS and 20 captioned shots.

Narration and captions are taken from the approved shot board.
All identifiers and diagrams are course demonstrations, not live evidence.
"""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "langfuse" / "build" / "lf03-xiaoxiao-v3"
BOARD = ROOT / "langfuse" / "LF-03-shot-board-xiaoxiao.md"
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
    ("01", "钩子", "类型记对了吗？", ["调用树", "类型"]),
    ("02", "反例", "都叫步骤，线索就没了", ["检索", "工具", "模型"]),
    ("03", "本集问题", "四种类型怎么选？", ["Span", "Generation", "Tool", "Agent"]),
    ("04", "Span · 步骤", "普通处理步骤", ["retrieve", "parse", "route"]),
    ("05", "耗时边界", "耗时不等于质量", ["时长示意", "质量未评估"]),
    ("06", "Generation · 生成", "模型生成单独记", ["prompt", "model", "output"]),
    ("07", "字段边界", "有字段才记录", ["unknown"]),
    ("08", "质量边界", "记录存在 ≠ 答案正确", ["记录", "质量"]),
    ("09", "Tool · 工具", "看名字、参数、结果、错误", ["以版本为准"]),
    ("10", "安全边界", "已记录 ≠ 一定安全", ["权限待检"]),
    ("11", "Agent · 调度", "调度单元，不是模型别名", ["子步骤"]),
    ("12", "完整性边界", "有节点 ≠ 全链路完整", ["需展开核对"]),
    ("13", "最小例子", "查资料 → 调工具 → 生成答案", ["固定输入"]),
    ("14", "类型流程", "每一步都有对应类型", ["Trace"]),
    ("15", "父子关系", "跟着真实调度走", ["禁止美化挪位"]),
    ("16", "验收清单", "核对类型、父节点和错误", ["unknown"]),
    ("17", "回读闭环", "同一个 Trace ID 核对", ["示意 ID"]),
    ("18", "范围边界", "单条树推不出整体稳定", ["多样本未证明"]),
    ("19", "本集边界", "示意不是验收通过", ["prototype / L1"]),
    ("20", "下一集", "Prompt 版本和 label", ["LF-04"]),
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
    pattern = re.compile(
        r"^\| (\d{2}) \| `([^\`]+)` \| [^|]+ \| (.*?) \| (.*?) \| (.*?) \|$",
        re.M,
    )
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
        raise ValueError("expected 20 shots with 20 unique layouts")
    return shots


SHOTS = load_shots()


def label(draw, text, xy, size=32, color=(237, 244, 255), light=False, max_w=880):
    return base.label(draw, text, xy, size, color, light, max_w)


def header(draw, shot, idx, accent, fg):
    draw.text((72, 62), f"LF-03  ·  {shot['kicker']}", font=u.font(28, True), fill=accent)
    label(draw, shot["title"], (72, 118), 54, fg, max_w=930)
    draw.text((72, 252), f"{idx:02d} / 20    prototype / L1", font=u.font(24, True), fill=(185, 195, 215))
    u.rounded(draw, (72, 304, 1008, 314), 5, (41, 48, 65))
    u.rounded(draw, (72, 304, 72 + int(936 * idx / 20), 314), 5, accent)


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
        node(d, (360, y), "Trace", accent, fg, 360, 120)
        node(d, (140, y + 240), "节点 A", accent, fg, 250, 120)
        node(d, (690, y + 240), "节点 B?", (255, 120, 130), fg, 250, 120)
        d.line((540, y + 120, 265, y + 240), fill=accent, width=4)
        d.line((540, y + 120, 815, y + 240), fill=(255, 120, 130), width=4)
        label(d, "类型记对了吗？", (250, y + 470), 54, accent)
        label(d, "树在，不等于节点都对", (230, y + 620), 38, fg)
    elif layout == "compare-blur":
        u.panel(d, (60, y + 20, 500, y + 700))
        label(d, "真实动作", (110, y + 70), 36, accent)
        for i, text in enumerate(["检索", "工具", "模型"]):
            node(d, (110, y + 170 + i * 160), text, accent, fg, 320, 120)
        u.panel(d, (560, y + 20, 1020, y + 700), (18, 20, 28))
        label(d, "都叫步骤", (640, y + 70), 36, (150, 155, 170))
        for i in range(3):
            u.rounded(d, (620, y + 190 + i * 150, 960, y + 290 + i * 150), 24, (55, 58, 70))
        label(d, "token / 参数 模糊", (610, y + 640), 28, (150, 155, 170), True)
    elif layout == "type-grid":
        for i, (en, zh) in enumerate([("Span", "步骤"), ("Generation", "生成"), ("Tool", "工具"), ("Agent", "调度")]):
            xx, yy = 70 + (i % 2) * 480, y + 20 + (i // 2) * 340
            u.panel(d, (xx, yy, xx + 440, yy + 290))
            label(d, en, (xx + 40, yy + 70), 48, accent)
            label(d, zh, (xx + 40, yy + 160), 36, fg)
        label(d, "分别什么时候用？", (320, y + 740), 40, fg)
    elif layout == "span-route":
        for i, text in enumerate(["retrieve", "parse", "route"]):
            xx = 80 + i * 310
            node(d, (xx, y + 220), text, accent, fg, 260, 150)
            if i < 2:
                base.arrow(d, (xx + 270, y + 295), (xx + 300, y + 295), accent)
        u.panel(d, (90, y + 500, 990, y + 680))
        label(d, "Span：开始 / 结束 / 输入输出", (150, y + 555), 40, fg)
    elif layout == "stopwatch":
        d.ellipse((360, y + 20, 720, y + 380), outline=accent, width=10)
        label(d, "时长", (460, y + 145), 64, accent)
        u.panel(d, (90, y + 450, 490, y + 680))
        u.panel(d, (590, y + 450, 990, y + 680))
        label(d, "输入 / 输出", (150, y + 530), 36, fg)
        label(d, "质量：留空", (670, y + 530), 36, (255, 140, 150))
        label(d, "耗时数字 ≠ 质量好坏", (250, y + 740), 38, accent)
    elif layout == "generation-stage":
        u.panel(d, (70, y + 20, 1010, y + 250), (20, 24, 36))
        label(d, "前序 Span 退到背景", (230, y + 105), 40, (160, 170, 190))
        for i, text in enumerate(["prompt", "model", "output"]):
            node(d, (90 + i * 310, y + 360), text, accent, fg, 270, 160)
            if i < 2:
                base.arrow(d, (360 + i * 310, y + 440), (390 + i * 310, y + 440), accent)
        label(d, "Generation 专记模型生成", (250, y + 620), 40, fg)
    elif layout == "metadata-card":
        u.panel(d, (80, y + 20, 1000, y + 730), (240, 244, 248))
        label(d, "GENERATION 字段", (140, y + 80), 40, (25, 50, 75))
        for i, (name, value) in enumerate([
            ("model", "看原始字段"),
            ("input / output", "看原始字段"),
            ("token / cost", "unknown"),
            ("usage", "未提供则不补数"),
        ]):
            yy = y + 190 + i * 120
            label(d, name, (150, yy), 36, (30, 45, 65))
            label(d, value, (620, yy), 32, (185, 55, 75) if "unknown" in value or "未提供" in value else (35, 120, 105))
    elif layout == "verdict-split":
        u.panel(d, (60, y + 80, 490, y + 560))
        u.panel(d, (590, y + 80, 1020, y + 560))
        label(d, "记录存在", (145, y + 250), 48, fg)
        label(d, "答案正确？", (655, y + 250), 48, fg)
        label(d, "≠", (495, y + 250), 78, (255, 112, 120))
        label(d, "质量仍要单独评估", (300, y + 680), 40, accent)
    elif layout == "tool-call":
        node(d, (360, y), "Tool", accent, fg, 360, 130)
        for i, text in enumerate(["name", "args", "result", "error"]):
            xx, yy = 80 + (i % 2) * 470, y + 230 + (i // 2) * 230
            u.panel(d, (xx, yy, xx + 430, yy + 180))
            label(d, text, (xx + 40, yy + 60), 44, fg)
        label(d, "以当前 SDK / 部署版本为准", (230, y + 750), 34, accent)
    elif layout == "shield-boundary":
        d.polygon([(540, y + 20), (820, y + 160), (740, y + 470), (340, y + 470), (260, y + 160)], outline=accent, width=8)
        node(d, (390, y + 180), "工具节点", accent, fg, 300, 140)
        u.panel(d, (90, y + 540, 990, y + 720))
        label(d, "权限 / 输入边界 / 失败处理：待检", (130, y + 595), 36, (255, 140, 150))
    elif layout == "agent-orbit":
        d.ellipse((250, y + 40, 830, y + 520), outline=accent, width=6)
        node(d, (390, y + 180), "Agent 调度", accent, fg, 300, 140)
        for i, text in enumerate(["子步骤", "子步骤", "子步骤"]):
            xx = 90 + i * 310
            node(d, (xx, y + 600), text, accent, fg, 250, 120)
        label(d, "圈外模型 ≠ 自动叫 Agent", (250, y + 760), 34, accent)
    elif layout == "nested-window":
        d.rounded_rectangle((80, y + 20, 1000, y + 700), radius=28, outline=accent, width=5)
        label(d, "Agent 外层窗口", (140, y + 60), 40, accent)
        for i, text in enumerate(["子步骤 1", "子步骤 2", "缺口 / 虚线"]):
            yy = y + 180 + i * 150
            if i < 2:
                node(d, (180, yy), text, accent, fg, 720, 120)
            else:
                d.rounded_rectangle((180, yy, 900, yy + 120), radius=24, outline=(120, 130, 150), width=3)
                label(d, text, (360, yy + 35), 36, (170, 180, 200))
    elif layout == "scenario-strip":
        for i, text in enumerate(["固定问题", "查资料 / 工具", "生成答案"]):
            node(d, (90, y + 40 + i * 220), text, accent, fg, 900, 160)
            if i < 2:
                d.polygon([(540, y + 210 + i * 220), (580, y + 210 + i * 220), (560, y + 245 + i * 220)], fill=accent)
        label(d, "最小例子 · 固定输入", (300, y + 740), 38, fg)
    elif layout == "typed-flow":
        pairs = [("Trace", "整次请求"), ("Span", "检索"), ("Tool", "工具"), ("Generation", "模型回答")]
        for i, (typ, name) in enumerate(pairs):
            xx = 40 + i * 255
            node(d, (xx, y + 180), name, accent, fg, 230, 140)
            label(d, typ, (xx + 20, y + 360), 30, accent, True, 200)
            if i < 3:
                base.arrow(d, (xx + 235, y + 250), (xx + 250, y + 250), accent)
        label(d, "不画虚假耗时", (370, y + 560), 40, fg)
    elif layout == "tree":
        node(d, (360, y), "Trace", accent, fg, 360, 120)
        node(d, (120, y + 240), "Agent / Span", accent, fg, 360, 130)
        node(d, (600, y + 240), "Span", accent, fg, 300, 130)
        node(d, (80, y + 500), "Generation", accent, fg, 300, 130)
        node(d, (430, y + 500), "Tool", accent, fg, 250, 130)
        d.line((540, y + 120, 300, y + 240), fill=accent, width=4)
        d.line((540, y + 120, 750, y + 240), fill=accent, width=4)
        d.line((300, y + 370, 230, y + 500), fill=accent, width=4)
        d.line((300, y + 370, 555, y + 500), fill=accent, width=4)
        label(d, "禁止为了好看去挪节点", (250, y + 700), 36, (255, 140, 150))
    elif layout == "checklist":
        items = ["type", "name", "parentObservationId", "input / output", "error", "usage → unknown"]
        for i, text in enumerate(items):
            yy = y + i * 110
            d.rounded_rectangle((90, yy, 150, yy + 60), radius=8, outline=accent, width=3)
            label(d, text, (190, yy + 10), 36, fg, max_w=780)
    elif layout == "loop":
        for i, text in enumerate(["发出请求", "拿到 Trace ID", "同一记录回读"]):
            node(d, (140, y + i * 210), text, accent, fg, 800, 150)
            if i < 2:
                d.polygon([(520, y + 163 + i * 210), (560, y + 163 + i * 210), (540, y + 198 + i * 210)], fill=accent)
        label(d, "示意 ID：tr_demo_003", (300, y + 680), 36, accent)
    elif layout == "trend":
        u.panel(d, (60, y + 30, 490, y + 650))
        label(d, "这一次", (150, y + 90), 40, fg)
        node(d, (130, y + 250), "类型挂对", accent, fg, 280, 140)
        u.panel(d, (590, y + 30, 1020, y + 650))
        label(d, "多次运行", (680, y + 90), 40, fg)
        d.rectangle((650, y + 220, 960, y + 470), outline=(90, 100, 125), width=3)
        label(d, "尚无证据", (700, y + 320), 36, (255, 125, 135))
        label(d, "推不出整体稳定或模型更好", (180, y + 740), 36, accent)
    elif layout == "stamp":
        u.panel(d, (72, y + 45, 1008, y + 710), (40, 17, 24))
        label(d, "PROTOTYPE", (135, y + 115), 68, (255, 140, 150))
        label(d, "L1 / 课程示意", (135, y + 250), 54, fg)
        for i, text in enumerate(["写入：未证明", "Worker 消费：未证明", "UI / API 回读：未证明"]):
            label(d, text, (135, y + 390 + i * 80), 34, (255, 170, 180))
    elif layout == "cta":
        u.panel(d, (72, y + 55, 1008, y + 720), tuple(int(c * .35) for c in accent))
        label(d, "下一集 / LF-04", (130, y + 115), 38, fg)
        label(d, "Prompt 版本", (180, y + 280), 58, fg)
        label(d, "label", (180, y + 400), 58, accent)
        label(d, "实验才有可比起点", (180, y + 560), 40, fg)
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
    video = ROOT / "langfuse/videos/LF-03-span-generation-xiaoxiao-v3.mp4"
    base.run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
              "-i", str(concat), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
              "-b:a", "128k", "-movflags", "+faststart", str(video)])
    srt, vtt = [], ["WEBVTT", ""]
    for i, item in enumerate(timeline, start=1):
        srt += [str(i), f"{base.ts(item['start'], True)} --> {base.ts(item['end'], True)}", item["caption"], ""]
        vtt += [f"{base.ts(item['start'])} --> {base.ts(item['end'])}", item["caption"], ""]
    srt_path = ROOT / "langfuse/captions/LF-03-xiaoxiao-v3.srt"
    vtt_path = ROOT / "langfuse/captions/LF-03-xiaoxiao-v3.vtt"
    srt_path.write_text("\n".join(srt), encoding="utf-8")
    vtt_path.write_text("\n".join(vtt), encoding="utf-8")
    (BUILD / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"video": str(video), "duration": base.duration(video), "shots": len(timeline),
                      "last_caption_end": timeline[-1]["end"]}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
