#!/usr/bin/env python3
"""Render LF-01 Xiaoxiao v3: original-speed neural TTS, unique shots, burned captions."""
from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "langfuse" / "build" / "lf01-xiaoxiao-v3"
VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "-5%"
EDGE = Path("/tmp/ttsvenv/bin/edge-tts")
FFMPEG = "/opt/homebrew/opt/ffmpeg@7/bin/ffmpeg"
FFPROBE = "/opt/homebrew/opt/ffmpeg@7/bin/ffprobe"
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_LIGHT = "/System/Library/Fonts/STHeiti Light.ttc"
W, H = 1080, 1920

SHOTS = [
    {
        "id": "01",
        "layout": "hook",
        "title": "错在哪一步？",
        "kicker": "钩子",
        "lines": ["你的模型答错了", "最后一句答案不够"],
        "voice": "你的模型答错了。你知道错在哪一步吗？",
        "caption": "你的模型答错了。你知道错在哪一步吗？",
        "chips": ["模型输出", "看不见过程"],
    },
    {
        "id": "02",
        "layout": "split",
        "title": "只看答案会漏掉过程",
        "kicker": "问题",
        "left": ["最后一句", "看起来完整", "不知道卡在哪"],
        "right": ["全过程", "检索 / 工具 / 生成", "能回头检查"],
        "voice": "只看最后一句答案，通常看不出来。",
        "caption": "只看最后一句答案，通常看不出来。",
        "chips": ["答案", "过程"],
    },
    {
        "id": "03",
        "layout": "statement",
        "title": "Langfuse 先把过程记下",
        "kicker": "定义",
        "lines": ["记录一次请求", "方便你回头检查", "而不是先做排行榜"],
        "voice": "Langfuse 做的事很简单：把一次请求的过程记录下来，让你能回头检查。",
        "caption": "把一次请求的过程记录下来，让你能回头检查。",
        "chips": ["记录", "复查"],
    },
    {
        "id": "04",
        "layout": "pipeline",
        "title": "一条最小链路",
        "kicker": "流程",
        "steps": ["提问", "检索", "工具", "模型", "答案"],
        "voice": "先看一条最小链路：用户提问，系统检索资料，再调用工具，最后让模型生成答案。少了任何一步，最后那句答案都解释不清。",
        "caption": "提问 → 检索 → 工具 → 模型 → 答案",
        "chips": ["最小链路"],
    },
    {
        "id": "05",
        "layout": "card",
        "title": "Trace = 一次完整请求",
        "kicker": "Trace",
        "lines": ["从请求开始到请求结束", "像一份完整的就诊记录", "不是散落的几行日志"],
        "voice": "这一整次请求，叫一条 Trace。你可以把它理解成一次完整的就诊记录。",
        "caption": "Trace：一次完整请求，像一份就诊记录。",
        "chips": ["Trace", "request start → end"],
    },
    {
        "id": "06",
        "layout": "nested",
        "title": "Trace 里面还有步骤",
        "kicker": "Span",
        "lines": ["更细的步骤叫 Span", "一步一步拆开看", "慢、空、报错都能定位"],
        "voice": "Trace 里面还有更细的步骤。每一个步骤，叫一个 Span。",
        "caption": "Trace 里的每一步，叫一个 Span。",
        "chips": ["Span"],
    },
    {
        "id": "07",
        "layout": "trio",
        "title": "常见三种 Span",
        "kicker": "步骤",
        "cards": [
            ("retrieve", "检索资料"),
            ("parse", "解析结果"),
            ("tool", "调用工具"),
        ],
        "voice": "比如 retrieve 是检索，parse 是解析，tool 是工具调用。哪一步变慢、哪一步空了、哪一步报错，一眼就能定位。",
        "caption": "retrieve / parse / tool，哪一步出问题一眼能定位。",
        "chips": ["耗时", "空结果", "报错"],
    },
    {
        "id": "08",
        "layout": "generation",
        "title": "Generation 是模型那一步",
        "kicker": "Generation",
        "steps": ["prompt", "model", "output"],
        "voice": "模型真正生成文字的那一步，通常标成 Generation。它会带上输入、输出和模型信息。",
        "caption": "Generation：prompt → model → output。",
        "chips": ["输入", "输出", "模型"],
    },
    {
        "id": "09",
        "layout": "before_after",
        "title": "看到答案怎么来的",
        "kicker": "对照",
        "left": ["以前", "只有最终答案"],
        "right": ["现在", "答案 + 来路"],
        "voice": "于是你不只看到答案是什么，还看到答案是怎么来的。",
        "caption": "不只看到答案是什么，还看到答案是怎么来的。",
        "chips": ["结果", "来路"],
    },
    {
        "id": "10",
        "layout": "score",
        "title": "记录之后才能打分",
        "kicker": "Score",
        "cards": [("correctness", "对不对"), ("format", "格式对不对"), ("feedback", "用户怎么说")],
        "voice": "接下来，你可以把这些记录按正确性、格式和用户反馈打分。",
        "caption": "按正确性、格式和用户反馈打分。",
        "chips": ["Score"],
    },
    {
        "id": "11",
        "layout": "samples",
        "title": "把感觉不好变成样本",
        "kicker": "失败样本",
        "lines": ["低分要能打开", "能看到当时输入输出", "能复查，而不是口头吐槽"],
        "voice": "这一步的价值，是把感觉不好，变成可以复查的失败样本。",
        "caption": "把“感觉不好”变成可以复查的失败样本。",
        "chips": ["低分", "可复查"],
    },
    {
        "id": "12",
        "layout": "warning",
        "title": "页面打开 ≠ 写入成功",
        "kicker": "边界",
        "lines": ["能打开页面", "不等于链路已写入", "更不等于已经处理完"],
        "voice": "但要注意，页面能打开，不代表链路已经写入成功。",
        "caption": "页面能打开，不代表链路已经写入成功。",
        "chips": ["UI", "写入"],
    },
    {
        "id": "13",
        "layout": "not_equal",
        "title": "health 200 不是 Trace",
        "kicker": "健康检查",
        "left": "health 200",
        "right": "new Trace",
        "voice": "例如 health 返回 200，只能说明健康检查在那个时间点通过。",
        "caption": "health 200，只说明当时健康检查通过。",
        "chips": ["时间点采样"],
    },
    {
        "id": "14",
        "layout": "blocked",
        "title": "Worker 和回读仍未证明",
        "kicker": "未证明",
        "cards": [("Trace 写入", "未证明"), ("Worker 消费", "未证明"), ("回读核对", "未证明")],
        "voice": "它不能证明刚才那条 Trace 已经写进去，更不能证明后台任务处理完成。",
        "caption": "不能证明 Trace 已写入，也不能证明后台任务完成。",
        "chips": ["BLOCKED"],
    },
    {
        "id": "15",
        "layout": "loop",
        "title": "最小证据闭环",
        "kicker": "验收",
        "steps": ["留下请求", "拿到 Trace ID", "同一条回读"],
        "voice": "真正验收时，要留下这次请求的记录，拿到 Trace ID，再用同一个 ID 把记录读回来核对。对不上，就不能说链路通了。",
        "caption": "请求 → Trace ID → 同一条回读。",
        "chips": ["ID 对得上"],
    },
    {
        "id": "16",
        "layout": "statement",
        "title": "先观察，再谈优化",
        "kicker": "第一层价值",
        "lines": ["先把过程看清楚", "再讨论改提示词", "再讨论换模型"],
        "voice": "这就是 Langfuse 的第一层价值：先观察，再讨论优化。",
        "caption": "先观察，再讨论优化。",
        "chips": ["观察", "优化"],
    },
    {
        "id": "17",
        "layout": "tree",
        "title": "Trace 帮你定位步骤",
        "kicker": "Trace 的用处",
        "lines": ["Trace", "├─ Span: retrieve", "└─ Generation: model"],
        "voice": "有了 Trace，你能定位问题发生在哪一步。",
        "caption": "有了 Trace，你能定位问题发生在哪一步。",
        "chips": ["定位"],
    },
    {
        "id": "18",
        "layout": "bars",
        "title": "Span 用来比耗时",
        "kicker": "Span 的用处",
        "bars": [("retrieve", 0.45), ("parse", 0.22), ("tool", 0.78)],
        "voice": "有了 Span，你能比较每个步骤的耗时和输入输出。",
        "caption": "Span 用来比较每一步的耗时和输入输出。",
        "chips": ["耗时", "输入输出"],
    },
    {
        "id": "19",
        "layout": "cost",
        "title": "Generation 看调用和成本",
        "kicker": "Generation 的用处",
        "cards": [("model", "用了哪个模型"), ("tokens", "输入 / 输出量"), ("cost", "这次花了多少")],
        "voice": "有了 Generation，你能分析模型调用、token 和成本。",
        "caption": "Generation 用来看模型调用、token 和成本。",
        "chips": ["token", "cost"],
    },
    {
        "id": "20",
        "layout": "compare_log",
        "title": "日志散落，Trace 成树",
        "kicker": "对照",
        "left": ["12:01 retrieve", "12:01 tool", "12:02 answer"],
        "right": ["Trace", " ├ retrieve", " └ generation"],
        "voice": "日志是一行一行散落的。Trace 把一次请求收成一棵树。",
        "caption": "日志是散落的行，Trace 是一棵请求树。",
        "chips": ["日志", "树"],
    },
    {
        "id": "21",
        "layout": "guess",
        "title": "没有树就只能猜",
        "kicker": "反例",
        "cards": [("检索差？", "不知道"), ("工具差？", "不知道"), ("模型差？", "不知道")],
        "voice": "没有这棵树，你只能猜是检索差、工具差，还是模型差。",
        "caption": "没有这棵树，你只能猜问题出在哪。",
        "chips": ["猜", "定位"],
    },
    {
        "id": "22",
        "layout": "rules",
        "title": "第一课只记三件事",
        "kicker": "收束",
        "cards": [("1", "先记过程"), ("2", "再打分"), ("3", "最后才优化")],
        "voice": "所以第一课记住三件事：先记过程，再打分，最后才谈优化。",
        "caption": "先记过程，再打分，最后才谈优化。",
        "chips": ["顺序"],
    },
    {
        "id": "23",
        "layout": "stamp",
        "title": "本集只建立概念",
        "kicker": "证据边界",
        "lines": ["prototype / L1", "画面是课程示意", "不是当前实例全链路验收"],
        "voice": "本集只建立概念。画面是 prototype、L1 示意，不代表当前实例已经完成全链路验收。",
        "caption": "prototype / L1：示意，不是全链路验收。",
        "chips": ["L1"],
    },
    {
        "id": "24",
        "layout": "cta",
        "title": "下一集拆开 Trace",
        "kicker": "预告",
        "lines": ["Trace 和普通日志", "到底差在哪里", "下一集继续"],
        "voice": "打开页面、截一张图、health 通过，都还不够当发布证据。下一集我们专门拆开 Trace：它和普通日志，到底差在哪里？",
        "caption": "下一集：Trace 和普通日志到底差在哪里？",
        "chips": ["LF-02"],
    },
]

PALETTES = [
    ((18, 18, 32), (91, 140, 255), (240, 244, 255)),
    ((16, 24, 38), (255, 176, 72), (255, 244, 230)),
    ((14, 28, 32), (72, 214, 186), (230, 255, 248)),
    ((28, 16, 36), (198, 146, 255), (246, 236, 255)),
    ((32, 18, 18), (255, 107, 129), (255, 236, 240)),
    ((12, 22, 40), (80, 180, 255), (232, 244, 255)),
    ((22, 18, 12), (255, 196, 84), (255, 246, 228)),
    ((10, 26, 22), (64, 220, 168), (228, 255, 244)),
]


def run(cmd, **kwargs):
    return subprocess.run(cmd, check=True, text=True, capture_output=True, **kwargs)


def duration(path: Path) -> float:
    out = subprocess.check_output(
        [FFPROBE, "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        text=True,
    ).strip()
    return float(out)


def font(size: int, light: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_LIGHT if light else FONT, size)


def wrap(draw: ImageDraw.ImageDraw, text: str, fnt, max_w: int) -> list[str]:
    lines, cur = [], ""
    for ch in text:
        trial = cur + ch
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines or [""]


def rounded(draw, xy, r, fill):
    draw.rounded_rectangle(xy, radius=r, fill=fill)


def header(draw, shot, idx, total, accent, fg):
    f_kicker = font(28, light=True)
    f_title = font(54)
    f_meta = font(24, light=True)
    draw.text((72, 70), f"LF-01  ·  {shot['kicker']}", font=f_kicker, fill=accent)
    title_lines = wrap(draw, shot["title"], f_title, W - 140)
    y = 120
    for line in title_lines[:2]:
        draw.text((72, y), line, font=f_title, fill=fg)
        y += 70
    draw.text((72, 250), f"{idx:02d} / {total:02d}    prototype / L1", font=f_meta, fill=(180, 190, 210))
    # progress
    bar_y = 300
    rounded(draw, (72, bar_y, W - 72, bar_y + 10), 5, (40, 48, 64))
    frac = idx / total
    rounded(draw, (72, bar_y, 72 + int((W - 144) * frac), bar_y + 10), 5, accent)
    return 340


def chips(draw, items, y, accent, fg):
    f = font(26)
    x = 72
    for item in items:
        tw = draw.textlength(item, font=f)
        rounded(draw, (x, y, x + tw + 36, y + 52), 26, (*accent, ) if False else tuple(int(c * 0.35 + 20) for c in accent))
        draw.text((x + 18, y + 10), item, font=f, fill=fg)
        x += int(tw) + 52
        if x > W - 200:
            x = 72
            y += 66
    return y + 70


def caption_box(draw, text, accent, fg):
    f = font(36)
    lines = wrap(draw, text, f, W - 180)
    box_h = 48 + 50 * len(lines)
    top = H - 220 - (box_h - 120)
    rounded(draw, (48, top, W - 48, H - 70), 28, (8, 10, 16))
    rounded(draw, (48, top, 60, H - 70), 8, accent)
    y = top + 28
    for line in lines[:3]:
        draw.text((84, y), line, font=f, fill=fg)
        y += 50


def panel(draw, xy, fill=(12, 16, 28)):
    rounded(draw, xy, 28, fill)


def draw_shot(shot, idx, total) -> Image.Image:
    bg, accent, fg = PALETTES[idx % len(PALETTES)]
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    y = header(d, shot, idx, total, accent, fg)
    layout = shot["layout"]
    f_big = font(44)
    f_mid = font(36)
    f_small = font(30, light=True)

    if layout == "hook":
        panel(d, (72, y + 20, W - 72, y + 520), (8, 10, 20))
        d.text((110, y + 80), "错在哪一步？", font=font(86), fill=fg)
        d.text((110, y + 220), "最后一句答案", font=f_big, fill=accent)
        d.text((110, y + 300), "看不见中间过程", font=f_big, fill=fg)
    elif layout == "split":
        panel(d, (72, y + 20, 504, y + 620))
        panel(d, (576, y + 20, W - 72, y + 620), tuple(int(c * 0.5 + 20) for c in accent))
        d.text((100, y + 50), shot["left"][0], font=f_big, fill=accent)
        for i, line in enumerate(shot["left"][1:]):
            d.text((100, y + 150 + i * 70), line, font=f_mid, fill=fg)
        d.text((610, y + 50), shot["right"][0], font=f_big, fill=fg)
        for i, line in enumerate(shot["right"][1:]):
            d.text((610, y + 150 + i * 70), line, font=f_mid, fill=fg)
    elif layout == "pipeline":
        steps = shot["steps"]
        box_w = 160
        gap = 18
        x0 = 72
        for i, step in enumerate(steps):
            x = x0 + i * (box_w + gap)
            panel(d, (x, y + 180, x + box_w, y + 360), (8, 12, 24) if i % 2 == 0 else tuple(int(c * 0.4) for c in accent))
            tw = d.textlength(step, font=f_mid)
            d.text((x + (box_w - tw) / 2, y + 240), step, font=f_mid, fill=fg)
            if i < len(steps) - 1:
                d.polygon([(x + box_w + 2, y + 260), (x + box_w + gap - 2, y + 270), (x + box_w + 2, y + 280)], fill=accent)
    elif layout == "trio" or layout == "score" or layout == "guess" or layout == "cost" or layout == "blocked":
        cards = shot.get("cards") or []
        for i, (a, b) in enumerate(cards):
            top = y + 40 + i * 230
            panel(d, (72, top, W - 72, top + 200))
            d.text((110, top + 36), str(a), font=f_big, fill=accent)
            d.text((110, top + 110), str(b), font=f_mid, fill=fg)
    elif layout == "generation" or layout == "loop":
        steps = shot["steps"]
        for i, step in enumerate(steps):
            top = y + 50 + i * 210
            panel(d, (72, top, W - 72, top + 180))
            d.text((110, top + 30), f"{i+1:02d}", font=font(28, True), fill=accent)
            d.text((110, top + 80), step, font=font(56), fill=fg)
            if i < len(steps) - 1:
                d.polygon([(W // 2 - 18, top + 182), (W // 2 + 18, top + 182), (W // 2, top + 206)], fill=accent)
    elif layout == "before_after" or layout == "compare_log":
        panel(d, (72, y + 20, 504, y + 700))
        panel(d, (576, y + 20, W - 72, y + 700))
        d.text((100, y + 50), shot["left"][0], font=f_big, fill=(255, 140, 140))
        for i, line in enumerate(shot["left"][1:]):
            d.text((100, y + 160 + i * 80), line, font=f_mid, fill=fg)
        d.text((610, y + 50), shot["right"][0], font=f_big, fill=accent)
        for i, line in enumerate(shot["right"][1:]):
            d.text((610, y + 160 + i * 80), line, font=f_mid, fill=fg)
    elif layout == "not_equal":
        panel(d, (72, y + 80, 460, y + 420))
        panel(d, (620, y + 80, W - 72, y + 420))
        d.text((110, y + 200), shot["left"], font=f_big, fill=fg)
        d.text((700, y + 200), shot["right"], font=f_big, fill=fg)
        d.text((490, y + 180), "≠", font=font(96), fill=(255, 110, 110))
    elif layout == "tree":
        panel(d, (72, y + 40, W - 72, y + 620))
        for i, line in enumerate(shot["lines"]):
            d.text((120, y + 100 + i * 120), line, font=font(48), fill=accent if i == 0 else fg)
    elif layout == "bars":
        for i, (name, frac) in enumerate(shot["bars"]):
            top = y + 80 + i * 180
            d.text((72, top), name, font=f_mid, fill=fg)
            rounded(d, (72, top + 60, W - 72, top + 110), 18, (20, 24, 36))
            rounded(d, (72, top + 60, 72 + int((W - 144) * frac), top + 110), 18, accent)
    elif layout == "rules":
        for i, (num, text) in enumerate(shot["cards"]):
            top = y + 40 + i * 230
            panel(d, (72, top, W - 72, top + 200))
            d.ellipse((110, top + 50, 190, top + 130), fill=accent)
            tw = d.textlength(num, font=f_big)
            d.text((150 - tw / 2, top + 68), num, font=f_big, fill=(10, 12, 18))
            d.text((230, top + 70), text, font=font(48), fill=fg)
    elif layout == "stamp":
        panel(d, (72, y + 80, W - 72, y + 620), (40, 16, 16))
        d.text((120, y + 160), "PROTOTYPE", font=font(64), fill=(255, 150, 150))
        d.text((120, y + 260), "L1 示意，不是验收通过", font=f_big, fill=fg)
        d.text((120, y + 360), "health / 截图 / 打开页面", font=f_mid, fill=(220, 200, 200))
        d.text((120, y + 430), "都不能代替回读", font=f_mid, fill=(220, 200, 200))
    elif layout == "cta":
        panel(d, (72, y + 80, W - 72, y + 620), tuple(int(c * 0.35) for c in accent))
        d.text((120, y + 160), "下一集 LF-02", font=font(40, True), fill=fg)
        d.text((120, y + 240), "Trace vs 日志", font=font(64), fill=fg)
        d.text((120, y + 360), "先把过程看清楚", font=f_big, fill=accent)
    else:
        panel(d, (72, y + 40, W - 72, y + 620))
        for i, line in enumerate(shot.get("lines") or []):
            d.text((110, y + 90 + i * 90), line, font=f_big, fill=fg)

    chips(d, shot.get("chips") or [], H - 360, accent, fg)
    caption_box(d, shot["caption"], accent, fg)
    return img


def synth(text: str, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    run([str(EDGE), "-v", VOICE, f"--rate={RATE}", "-t", text, "--write-media", str(dest)])


def make_silence(path: Path, seconds: float):
    run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", f"{seconds:.3f}",
        "-c:a", "aac", "-b:a", "96k", str(path),
    ])


def encode_clip(png: Path, audio: Path, out: Path, seconds: float):
    run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-loop", "1", "-framerate", "30", "-t", f"{seconds:.3f}", "-i", str(png),
        "-i", str(audio),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-vf", "scale=1080:1920",
        "-c:a", "aac", "-b:a", "128k", "-shortest",
        "-movflags", "+faststart", str(out),
    ])


def srt_ts(t: float) -> str:
    if t < 0:
        t = 0
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".", ",")


def vtt_ts(t: float) -> str:
    if t < 0:
        t = 0
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h:02d}:{m:02d}:{s:06.3f}"


def main() -> int:
    BUILD.mkdir(parents=True, exist_ok=True)
    audio_dir = BUILD / "audio"
    frame_dir = BUILD / "frames"
    clip_dir = BUILD / "clips"
    for p in (audio_dir, frame_dir, clip_dir):
        p.mkdir(exist_ok=True)

    timeline = []
    t = 0.0
    concat_lines = []
    gap = 0.22
    for i, shot in enumerate(SHOTS, start=1):
        wav = audio_dir / f"{shot['id']}.mp3"
        if not wav.exists() or wav.stat().st_size < 1000:
            synth(shot["voice"], wav)
        dur = duration(wav)
        png = frame_dir / f"{shot['id']}.png"
        draw_shot(shot, i, len(SHOTS)).save(png, "PNG")
        clip = clip_dir / f"{shot['id']}.mp4"
        encode_clip(png, wav, clip, dur)
        timeline.append({"id": shot["id"], "start": t, "end": t + dur, "caption": shot["caption"], "voice": shot["voice"]})
        concat_lines.append(f"file '{clip}'")
        t += dur
        if i != len(SHOTS):
            # tiny visual hold is already in clip; add tiny audio gap by concatenating silence video?
            # Keep speech tight: no extra silent video pad.
            t += 0.0

    concat_list = BUILD / "concat.txt"
    concat_list.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")
    out_mp4 = ROOT / "langfuse" / "videos" / "LF-01-langfuse-overview-xiaoxiao-v3.mp4"
    run([
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(concat_list),
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
        "-movflags", "+faststart", str(out_mp4),
    ])

    srt_path = ROOT / "langfuse" / "captions" / "LF-01-xiaoxiao-v3.srt"
    vtt_path = ROOT / "langfuse" / "captions" / "LF-01-xiaoxiao-v3.vtt"
    srt = []
    vtt = ["WEBVTT", ""]
    for n, item in enumerate(timeline, start=1):
        srt += [str(n), f"{srt_ts(item['start'])} --> {srt_ts(item['end'])}", item["caption"], ""]
        vtt += [f"{vtt_ts(item['start'])} --> {vtt_ts(item['end'])}", item["caption"], ""]
    srt_path.write_text("\n".join(srt), encoding="utf-8")
    vtt_path.write_text("\n".join(vtt), encoding="utf-8")
    (BUILD / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"video": str(out_mp4), "duration": duration(out_mp4), "shots": len(timeline), "last_caption_end": timeline[-1]["end"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
