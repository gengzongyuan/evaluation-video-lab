#!/usr/bin/env python3
"""Render LF-02 at original Xiaoxiao speed with 20 shots and burned captions.

Reads no runtime credentials. The tr_demo_001 identifier is explicitly a demo.
This script does not modify the LF-01 renderer or its assets.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import time
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "langfuse" / "build" / "lf02-xiaoxiao-v3"
EDGE = Path("/tmp/ttsvenv/bin/edge-tts")
VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-5%"
W, H = 1080, 1920

# Reuse only the existing LF-01 drawing primitives; no shared file is modified.
_spec = importlib.util.spec_from_file_location(
    "_lf01_drawing_primitives", ROOT / "langfuse/scripts/render_lf01_xiaoxiao_v3.py"
)
u = importlib.util.module_from_spec(_spec)
assert _spec.loader
_spec.loader.exec_module(u)
FFMPEG = u.FFMPEG
FFPROBE = u.FFPROBE

SHOTS = [
    dict(id="01", layout="hook", kicker="钩子", title="错在哪一步？",
         voice="用户只发了一句话。后台可能已经跑完检索、工具和模型。只看最终答案，你看不出哪一步出错。",
         caption="只看最终答案，看不出哪一步出错", chips=["一句话输入", "三步过程"]),
    dict(id="02", layout="compare-log", kicker="普通日志", title="中间过程是黑的",
         voice="普通日志常常只留下一句请求失败，或者一句最终回复。中间过程是黑的。",
         caption="普通日志常常只留下一句失败", chips=["request failed", "过程不可见"]),
    dict(id="03", layout="record-card", kicker="Trace · 追踪", title="一整次请求，记成一条 Trace",
         voice="Langfuse 把这一整次请求记成一条 Trace，追踪。你可以把它理解成一次完整的就诊记录。",
         caption="Trace：一次完整请求，像就诊记录", chips=["request start", "request end"]),
    dict(id="04", layout="nested-container", kicker="Trace", title="Trace 是容器，答案只占一角",
         voice="Trace 是容器，不是某一个模型答案。它把这次请求从头到尾串起来。",
         caption="Trace 是容器，不是某一个模型答案", chips=["容器", "完整过程"]),
    dict(id="05", layout="split", kicker="对照", title="散落日志 vs 调用树",
         voice="和普通日志的差别在这里：日志是一串散落的行，Trace 是一棵能展开的调用树。",
         caption="日志是散落的行，Trace 是一棵调用树", chips=["散落", "调用树"]),
    dict(id="06", layout="tree", kicker="Observation · 观察节点", title="树里每一个可观察动作",
         voice="树里每一个可观察动作，叫 Observation，观察节点。父节点下面还能挂子节点。",
         caption="Observation：树里每一个可观察动作", chips=["父节点", "子节点"]),
    dict(id="07", layout="span-card", kicker="Span · 步骤", title="检索、解析、工具，各是一步",
         voice="普通处理步骤，比如检索或工具调用，通常记成 Span，步骤。",
         caption="Span 用来记检索、解析、工具这些步骤", chips=["retrieve", "parse", "tool"]),
    dict(id="08", layout="generation", kicker="Generation · 生成", title="模型真正生成文字的那一步",
         voice="模型真正生成文字的那一步，记成 Generation，生成。它会带上输入、输出和模型信息。",
         caption="Generation：模型真正生成文字的那一步", chips=["prompt", "model", "output"]),
    dict(id="09", layout="bars", kicker="定位", title="从总耗时往下钻",
         voice="所以你能从总耗时往下钻：是检索慢，还是模型慢，还是工具报错。",
         caption="是检索慢、模型慢，还是工具报错", chips=["时长示意", "非实测"]),
    dict(id="10", layout="pipeline", kicker="最小链路", title="把一次请求串起来",
         voice="先看一条最小链路：用户提问，系统检索，再调用工具，最后模型生成答案。",
         caption="提问 → 检索 → 工具 → 模型 → 答案", chips=["一次请求"]),
    dict(id="11", layout="id-card", kicker="排错入口", title="先拿 Trace ID",
         voice="这整次请求共用一条 Trace ID。排错时先拿这个 ID，不要只翻终端滚动日志。",
         caption="排错先拿 Trace ID，不要只翻滚动日志", chips=["示意 ID", "禁止伪造"]),
    dict(id="12", layout="three-questions", kicker="排错三问", title="失败时，先问三句",
         voice="失败时先问三句：失败节点是哪一个？它的输入是什么？耗时和输出有没有异常？",
         caption="失败节点是哪一个？输入和输出有没有异常？", chips=["节点", "输入", "耗时 / 输出"]),
    dict(id="13", layout="inspect", kicker="逐项核对", title="别只看页面有没有数据",
         voice="打开这条 Trace，你要核对输入、输出、时间和状态，而不是只看页面有没有数据。",
         caption="要核对输入、输出、时间和状态", chips=["input", "output", "time", "status"]),
    dict(id="14", layout="warning", kicker="证据边界", title="页面打开 ≠ 写入成功",
         voice="但要注意，页面能打开，不代表刚才那条 Trace 已经写入成功。",
         caption="页面能打开，不代表 Trace 已经写入", chips=["UI", "写入未证明"]),
    dict(id="15", layout="not-equal", kicker="健康检查", title="health 200 ≠ 新 Trace",
         voice="例如 health 返回 200，只能说明健康检查在那个时间点通过。",
         caption="health 200 ≠ 新 Trace", chips=["时间点采样"]),
    dict(id="16", layout="blocked", kicker="仍未证明", title="写入和回读都不能省",
         voice="它不能证明新 Trace 已经写进去，更不能证明你能用同一个 ID 回读到同一条记录。",
         caption="不能证明新 Trace 已写入或可回读", chips=["BLOCKED"]),
    dict(id="17", layout="loop", kicker="验收闭环", title="同一个 ID，读回同一条",
         voice="真正验收时，要发出请求，拿到 Trace ID，再读取同一条记录核对。",
         caption="请求 → Trace ID → 同一条回读", chips=["同一 ID", "写入 + 回读"]),
    dict(id="18", layout="trend", kicker="范围边界", title="一条 Trace，不代表整体稳定",
         voice="还有一层边界：单条 Trace 只能说明这一次发生了什么，不能代表整体稳不稳定。",
         caption="单条 Trace 不能代表整体稳不稳定", chips=["单次", "整体未证明"]),
    dict(id="19", layout="stamp", kicker="本集边界", title="只讲差别，不伪装成验收",
         voice="本集只讲清 Trace 和普通日志的差别。画面是 prototype / L1 示意，不代表当前实例已经写入或回读成功。",
         caption="prototype / L1：示意，不是写入或回读成功", chips=["L1", "课程示意"]),
    dict(id="20", layout="cta", kicker="下一集", title="拆开 Span 和 Generation",
         voice="下一集我们拆开 Span 和 Generation：为什么模型调用要单独记？",
         caption="下一集：为什么模型调用要单独记？", chips=["LF-03", "模型调用"]),
]

PALETTES = [
    ((13, 20, 38), (89, 155, 255), (237, 244, 255)),
    ((29, 17, 30), (255, 141, 164), (255, 237, 245)),
    ((13, 29, 26), (75, 219, 169), (230, 255, 246)),
    ((30, 22, 13), (255, 192, 89), (255, 246, 227)),
    ((17, 21, 42), (166, 146, 255), (239, 237, 255)),
    ((27, 17, 19), (255, 114, 114), (255, 237, 239)),
]


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, check=True, text=True, capture_output=True)


def duration(path: Path) -> float:
    return float(run([FFPROBE, "-v", "error", "-show_entries", "format=duration",
                      "-of", "default=nw=1:nk=1", str(path)]).stdout.strip())


def label(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], size: int = 32,
          color=(237, 244, 255), light: bool = False, max_w: int = 880) -> int:
    f = u.font(size, light)
    x, y = xy
    lines = u.wrap(draw, text, f, max_w)
    for line in lines[:3]:
        draw.text((x, y), line, font=f, fill=color)
        y += int(size * 1.45)
    return y


def header(draw, shot, idx, accent, fg):
    draw.text((72, 62), f"LF-02  ·  {shot['kicker']}", font=u.font(28, True), fill=accent)
    label(draw, shot["title"], (72, 118), 54, fg, max_w=930)
    draw.text((72, 252), f"{idx:02d} / 20    prototype / L1", font=u.font(24, True), fill=(185, 195, 215))
    u.rounded(draw, (72, 304, 1008, 314), 5, (41, 48, 65))
    u.rounded(draw, (72, 304, 72 + int(936 * idx / 20), 314), 5, accent)


def node(draw, xy, text, accent, fg, width=260, height=140):
    x, y = xy
    u.panel(draw, (x, y, x + width, y + height), (9, 14, 26))
    lines = u.wrap(draw, text, u.font(34), width - 30)
    yy = y + (height - len(lines) * 48) / 2
    for line in lines[:2]:
        tw = draw.textlength(line, font=u.font(34))
        draw.text((x + (width - tw) / 2, yy), line, font=u.font(34), fill=fg)
        yy += 48
    draw.rounded_rectangle((x, y, x + width, y + height), radius=28, outline=accent, width=2)


def arrow(draw, start, end, accent):
    x1, y1 = start
    x2, y2 = end
    draw.line((x1, y1, x2, y2), fill=accent, width=5)
    draw.polygon([(x2, y2), (x2 - 15, y2 - 10), (x2 - 15, y2 + 10)], fill=accent)


def draw_shot(shot, idx):
    bg, accent, fg = PALETTES[(idx - 1) % len(PALETTES)]
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    header(d, shot, idx, accent, fg)
    y = 380
    layout = shot["layout"]
    if layout == "hook":
        node(d, (330, y), "用户的一句话", accent, fg, 420, 130)
        for i, text in enumerate(["检索", "工具", "模型"]):
            x = 90 + i * 330
            node(d, (x, y + 290), text + "  ?", accent, fg, 240, 160)
            d.line((540, y + 130, x + 120, y + 290), fill=(100, 112, 140), width=3)
        label(d, "后台跑完了，哪一步出错？", (130, y + 590), 48, accent)
    elif layout == "compare-log":
        u.panel(d, (72, y + 20, 508, y + 700), (4, 6, 11))
        label(d, "TERMINAL", (110, y + 65), 28, accent)
        label(d, "12:01:08", (110, y + 180), 30, fg)
        label(d, "request failed", (110, y + 245), 35, (255, 122, 137))
        label(d, "没有中间过程", (110, y + 360), 34, fg)
        u.panel(d, (556, y + 20, 1008, y + 700), (8, 10, 18))
        label(d, "过程", (600, y + 65), 30, fg)
        label(d, "？", (730, y + 210), 160, (95, 104, 130))
        label(d, "黑的", (700, y + 475), 42, (150, 158, 180))
    elif layout == "record-card":
        u.panel(d, (90, y + 10, 990, y + 730), (240, 244, 248))
        label(d, "TRACE / 追踪", (140, y + 60), 44, (24, 50, 74))
        d.line((140, y + 150, 940, y + 150), fill=(65, 110, 144), width=4)
        for i, (a, b) in enumerate([("请求开始", "已记录"), ("中间步骤", "可展开"), ("请求结束", "已记录")]):
            yy = y + 200 + i * 135
            label(d, a, (140, yy), 40, (24, 50, 74))
            label(d, b, (660, yy), 34, (35, 120, 106))
        label(d, "像一次完整的就诊记录", (140, y + 630), 35, (60, 75, 95))
    elif layout == "nested-container":
        u.panel(d, (72, y + 20, 1008, y + 760), (10, 15, 28))
        d.rounded_rectangle((72, y + 20, 1008, y + 760), radius=28, outline=accent, width=5)
        label(d, "Trace / 完整请求", (115, y + 60), 44, accent)
        for i, text in enumerate(["检索", "工具", "模型"]):
            node(d, (125 + i * 280, y + 210), text, accent, fg, 240, 140)
        label(d, "最终答案", (135, y + 470), 38, fg)
        u.panel(d, (450, y + 440, 900, y + 550), tuple(int(c * .4) for c in accent))
        label(d, "只占一角", (550, y + 470), 36, fg)
        label(d, "从头到尾串起来", (135, y + 640), 40, fg)
    elif layout == "split":
        u.panel(d, (72, y + 10, 492, y + 740))
        u.panel(d, (580, y + 10, 1008, y + 740))
        label(d, "日志 / 散落", (110, y + 60), 36, accent)
        for i, text in enumerate(["12:01 retrieve", "12:01 tool", "12:02 answer"]):
            label(d, text, (100, y + 200 + i * 105), 30, fg, max_w=365)
        label(d, "Trace / 树", (620, y + 60), 36, accent)
        for i, text in enumerate(["Trace", "├ retrieve", "├ tool", "└ generation"]):
            label(d, text, (620, y + 180 + i * 105), 32, fg, max_w=355)
    elif layout == "tree":
        node(d, (360, y), "Trace", accent, fg, 360, 125)
        node(d, (170, y + 250), "Observation", accent, fg, 330, 125)
        node(d, (580, y + 250), "Observation", accent, fg, 330, 125)
        node(d, (80, y + 530), "子节点", accent, fg, 240, 125)
        node(d, (380, y + 530), "子节点", accent, fg, 240, 125)
        node(d, (680, y + 530), "子节点", accent, fg, 240, 125)
        d.line((540, y + 125, 335, y + 250), fill=accent, width=4)
        d.line((540, y + 125, 745, y + 250), fill=accent, width=4)
        d.line((335, y + 375, 200, y + 530), fill=accent, width=4)
        d.line((335, y + 375, 500, y + 530), fill=accent, width=4)
        d.line((745, y + 375, 800, y + 530), fill=accent, width=4)
    elif layout == "span-card":
        for i, (en, zh) in enumerate([("retrieve", "检索"), ("parse", "解析"), ("tool", "工具调用")]):
            yy = y + i * 235
            u.panel(d, (72, yy, 1008, yy + 200))
            label(d, f"0{i+1}", (110, yy + 35), 30, accent)
            label(d, en, (220, yy + 35), 46, fg)
            label(d, zh, (220, yy + 110), 34, accent)
            label(d, "Span", (785, yy + 75), 35, fg)
    elif layout == "generation":
        for i, text in enumerate(["prompt / 输入", "model / 模型", "output / 输出"]):
            yy = y + i * 240
            u.panel(d, (120, yy, 960, yy + 175))
            label(d, f"0{i+1}", (160, yy + 55), 30, accent)
            label(d, text, (270, yy + 50), 46, fg)
            if i < 2:
                d.polygon([(525, yy + 185), (555, yy + 185), (540, yy + 220)], fill=accent)
    elif layout == "bars":
        for i, (name, frac) in enumerate([("retrieve", .33), ("tool / 报错", .66), ("generation", .91)]):
            yy = y + 40 + i * 220
            label(d, name, (72, yy), 38, fg)
            u.rounded(d, (72, yy + 75, 1008, yy + 135), 20, (25, 32, 48))
            color = (255, 100, 115) if i == 1 else accent
            u.rounded(d, (72, yy + 75, 72 + int(936 * frac), yy + 135), 20, color)
            label(d, "示意，非实测", (790, yy + 145), 24, (170, 180, 205), True)
    elif layout == "pipeline":
        for i, text in enumerate(["提问", "检索", "工具", "模型", "答案"]):
            xx = 52 + i * 202
            node(d, (xx, y + 230), text, accent, fg, 170, 160)
            if i < 4:
                arrow(d, (xx + 174, y + 310), (xx + 197, y + 310), accent)
        label(d, "同一条请求链路", (310, y + 540), 44, fg)
    elif layout == "id-card":
        u.panel(d, (72, y + 80, 1008, y + 440), (8, 13, 26))
        label(d, "TRACE ID / 示意", (125, y + 130), 32, accent)
        label(d, "tr_demo_001", (125, y + 225), 60, fg)
        label(d, "仅用于解释，不是真实 Trace", (125, y + 330), 30, (185, 195, 215), True)
        label(d, "先拿 ID，再回读", (125, y + 530), 48, fg)
        label(d, "不要只翻滚动日志", (125, y + 630), 38, accent)
    elif layout == "three-questions":
        for i, text in enumerate(["失败节点是哪一个？", "它的输入是什么？", "耗时和输出异常吗？"]):
            yy = y + i * 235
            u.panel(d, (72, yy, 1008, yy + 200))
            d.ellipse((105, yy + 55, 185, yy + 135), fill=accent)
            label(d, str(i + 1), (131, yy + 64), 38, bg)
            label(d, text, (230, yy + 70), 38, fg, max_w=720)
    elif layout == "inspect":
        u.panel(d, (72, y + 10, 1008, y + 740))
        label(d, "打开 Trace 后核对", (120, y + 65), 42, accent)
        for i, text in enumerate(["输入 input", "输出 output", "时间 time", "状态 status"]):
            yy = y + 170 + i * 125
            d.rounded_rectangle((120, yy, 164, yy + 44), radius=8, outline=accent, width=3)
            label(d, text, (210, yy - 5), 38, fg)
    elif layout == "warning":
        u.panel(d, (72, y + 60, 1008, y + 480), (8, 12, 22))
        d.ellipse((120, y + 100, 140, y + 120), fill=(255, 114, 114))
        d.ellipse((155, y + 100, 175, y + 120), fill=(255, 192, 89))
        label(d, "页面已打开", (160, y + 220), 64, fg)
        d.line((750, y + 170, 920, y + 340), fill=(255, 100, 110), width=18)
        d.line((920, y + 170, 750, y + 340), fill=(255, 100, 110), width=18)
        label(d, "仍未证明 Trace 写入", (120, y + 600), 48, accent)
    elif layout == "not-equal":
        u.panel(d, (72, y + 160, 440, y + 520))
        u.panel(d, (640, y + 160, 1008, y + 520))
        label(d, "health", (155, y + 225), 48, fg)
        label(d, "200", (165, y + 315), 64, accent)
        label(d, "new", (750, y + 225), 48, fg)
        label(d, "Trace", (725, y + 315), 58, fg)
        label(d, "≠", (495, y + 285), 96, (255, 112, 120))
        label(d, "只说明当时健康检查通过", (120, y + 650), 40, fg)
    elif layout == "blocked":
        for i, text in enumerate(["新 Trace 写入", "同一 ID 回读", "同一条记录核对"]):
            yy = y + i * 230
            u.panel(d, (72, yy, 1008, yy + 190))
            label(d, text, (120, yy + 35), 40, fg)
            label(d, "未证明", (120, yy + 110), 32, (255, 115, 125))
            label(d, "×", (850, yy + 55), 60, (255, 115, 125))
    elif layout == "loop":
        for i, text in enumerate(["发出请求", "拿到 Trace ID", "读取同一条记录"]):
            yy = y + i * 225
            node(d, (170, yy), text, accent, fg, 740, 160)
            if i < 2:
                d.polygon([(520, yy + 173), (560, yy + 173), (540, yy + 210)], fill=accent)
        label(d, "ID 对不上，就不能说验收通过", (115, y + 735), 36, accent)
    elif layout == "trend":
        u.panel(d, (72, y + 20, 440, y + 650))
        label(d, "单条 Trace", (125, y + 80), 40, fg)
        d.ellipse((215, y + 290, 285, y + 360), fill=accent)
        label(d, "只说明这一次", (105, y + 450), 34, accent)
        u.panel(d, (560, y + 20, 1008, y + 650))
        label(d, "整体趋势", (635, y + 80), 40, fg)
        for i in range(6):
            d.line((625 + i * 50, y + 340 - (i % 3) * 45, 675 + i * 50, y + 340 - ((i + 1) % 3) * 45), fill=(130, 140, 170), width=3)
        label(d, "未证明", (655, y + 450), 48, (255, 125, 130))
    elif layout == "stamp":
        u.panel(d, (72, y + 60, 1008, y + 670), (40, 17, 24))
        label(d, "PROTOTYPE", (135, y + 135), 68, (255, 140, 150))
        label(d, "L1 / 课程示意", (135, y + 280), 54, fg)
        label(d, "不是当前实例", (135, y + 415), 42, fg)
        label(d, "写入或回读成功", (135, y + 490), 42, (255, 140, 150))
    elif layout == "cta":
        u.panel(d, (72, y + 70, 1008, y + 700), tuple(int(c * .4) for c in accent))
        label(d, "下一集 / LF-03", (130, y + 140), 36, fg)
        label(d, "Span", (130, y + 250), 68, fg)
        label(d, "Generation", (130, y + 360), 68, fg)
        label(d, "为什么模型调用要单独记？", (130, y + 525), 42, accent)
    else:
        raise ValueError(f"unknown layout: {layout}")
    u.chips(d, shot["chips"], H - 360, accent, fg)
    u.caption_box(d, shot["caption"], accent, fg)
    return im


def synth(text: str, dest: Path):
    cmd = [str(EDGE), "-v", VOICE, f"--rate={RATE}", "-t", text, "--write-media", str(dest)]
    for attempt in range(1, 4):
        p = subprocess.run(cmd, text=True, capture_output=True)
        if p.returncode == 0 and dest.stat().st_size > 1000:
            return
        if attempt == 3:
            raise RuntimeError(p.stderr or "edge-tts failed")
        time.sleep(1.5 * attempt)


def encode_clip(png: Path, audio: Path, out: Path, seconds: float):
    run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
         "-loop", "1", "-framerate", "30", "-t", f"{seconds:.3f}", "-i", str(png),
         "-i", str(audio), "-c:v", "libx264", "-pix_fmt", "yuv420p",
         "-vf", "scale=1080:1920", "-c:a", "aac", "-b:a", "128k", "-shortest",
         "-movflags", "+faststart", str(out)])


def ts(value: float, srt=False) -> str:
    h = int(value // 3600)
    m = int(value % 3600 // 60)
    s = value % 60
    out = f"{h:02d}:{m:02d}:{s:06.3f}"
    return out.replace(".", ",") if srt else out


def main() -> int:
    if len({s["id"] for s in SHOTS}) != 20 or len({s["layout"] for s in SHOTS}) != 20:
        raise ValueError("expected 20 unique shot ids and layouts")
    for name in ["audio", "frames", "clips"]:
        (BUILD / name).mkdir(parents=True, exist_ok=True)
    timeline, clips, start = [], [], 0.0
    for idx, shot in enumerate(SHOTS, start=1):
        audio = BUILD / "audio" / f"{shot['id']}.mp3"
        if not audio.exists() or audio.stat().st_size < 1000:
            synth(shot["voice"], audio)
        seconds = duration(audio)
        png = BUILD / "frames" / f"{shot['id']}.png"
        draw_shot(shot, idx).save(png, "PNG")
        clip = BUILD / "clips" / f"{shot['id']}.mp4"
        encode_clip(png, audio, clip, seconds)
        timeline.append({"id": shot["id"], "layout": shot["layout"], "start": start,
                         "end": start + seconds, "caption": shot["caption"], "voice": shot["voice"]})
        clips.append(clip)
        start += seconds
        print(f"shot {shot['id']}: {seconds:.3f}s / {shot['layout']}", flush=True)
    concat = BUILD / "concat.txt"
    concat.write_text("".join(f"file '{p}'\n" for p in clips), encoding="utf-8")
    video = ROOT / "langfuse/videos/LF-02-trace-xiaoxiao-v3.mp4"
    run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", str(concat), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
         "-b:a", "128k", "-movflags", "+faststart", str(video)])
    srt, vtt = [], ["WEBVTT", ""]
    for i, item in enumerate(timeline, start=1):
        srt += [str(i), f"{ts(item['start'], True)} --> {ts(item['end'], True)}", item["caption"], ""]
        vtt += [f"{ts(item['start'])} --> {ts(item['end'])}", item["caption"], ""]
    srt_path = ROOT / "langfuse/captions/LF-02-xiaoxiao-v3.srt"
    vtt_path = ROOT / "langfuse/captions/LF-02-xiaoxiao-v3.vtt"
    srt_path.write_text("\n".join(srt), encoding="utf-8")
    vtt_path.write_text("\n".join(vtt), encoding="utf-8")
    (BUILD / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"video": str(video), "duration": duration(video), "shots": len(timeline),
                      "last_caption_end": timeline[-1]["end"]}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
