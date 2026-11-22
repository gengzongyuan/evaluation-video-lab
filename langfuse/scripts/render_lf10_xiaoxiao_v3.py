#!/usr/bin/env python3
"""Render LF-10 Agent call tree with original-speed Xiaoxiao and burned captions."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "langfuse/build/lf10-xiaoxiao-v3"
BOARD = ROOT / "langfuse/LF-10-shot-board-xiaoxiao.md"
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
    ("01", "钩子", "最后一句答案，看不见 Agent 的过程", ["规划", "工具", "生成"]),
    ("02", "Agent 循环", "Agent 是多步工作单元，不是模型别名", ["规划", "执行"]),
    ("03", "Trace 容器", "一次请求，收进同一棵 Trace 树", ["空位待填"]),
    ("04", "调度映射", "父子关系跟着真实调度走", ["错挂打叉"]),
    ("05", "Span 卡", "检索和解析，先记成普通步骤", ["retrieve", "parse"]),
    ("06", "Tool", "Tool 记录一次真实外部能力调用", ["name", "args"]),
    ("07", "Generation", "Generation 单独记录模型调用", ["usage unknown"]),
    ("08", "迭代", "每一轮模型调用，都保留自己的节点", ["第二轮"]),
    ("09", "调用树", "把调度、工具和模型展开成一棵树", ["示意"]),
    ("10", "字段卡", "节点字段都要按版本核对", ["按当前版本核对"]),
    ("11", "失败节点", "错误要落在真实的失败节点上", ["Tool 标红"]),
    ("12", "脱敏", "输入输出和错误堆栈都要脱敏", ["公开只留结构"]),
    ("13", "瀑布", "树看结构，瀑布看时间花在哪里", ["耗时留空"]),
    ("14", "孤立节点", "孤立节点说明调用关系可能断了", ["parent 为空"]),
    ("15", "重复记录", "重复记录会污染耗时和统计", ["副本"]),
    ("16", "缺失分支", "树里没看到，不等于过程没发生", ["采样", "漏接"]),
    ("17", "回读闭环", "同一个 Trace ID 回读整棵树", ["四步"]),
    ("18", "决策门", "树完整 ≠ 决策正确或工具安全", ["质量", "权限"]),
    ("19", "本集边界", "不是 Agent 树已跑通", ["prototype / L1"]),
    ("20", "下一集", "同组样本比较 Prompt 或模型", ["LF-11"]),
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
    draw.text((72, 62), f"LF-10  ·  {shot['kicker']}", font=u.font(28, True), fill=accent)
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
        node(d, (90, y + 20), "用户的一句话", accent, fg, 900, 130)
        for i, text in enumerate(["规划", "检索", "工具", "生成"]):
            node(d, (70 + i * 250, y + 280), text, accent, fg, 220, 150)
        label(d, "最后一句只占一角", (240, y + 520), 40, fg)
        u.panel(d, (240, y + 590, 840, y + 720), tuple(int(c * .35) for c in accent))
        label(d, "最终答案", (390, y + 625), 40, fg)
    elif layout == "agent-loop":
        for i, text in enumerate(["规划", "执行", "观察", "再规划"]):
            xx, yy = 90 + (i % 2) * 460, y + 40 + (i // 2) * 280
            node(d, (xx, yy), text, accent, fg, 400, 180)
        label(d, "模型只占其中一格", (280, y + 650), 36, fg)
    elif layout == "trace-container":
        u.panel(d, (72, y + 20, 1008, y + 720))
        d.rounded_rectangle((72, y + 20, 1008, y + 720), radius=28, outline=accent, width=5)
        label(d, "Trace", (120, y + 60), 44, accent)
        for i, text in enumerate(["Agent", "检索", "工具", "模型"]):
            xx = 120 + (i % 2) * 430
            yy = y + 180 + (i // 2) * 220
            node(d, (xx, yy), text + " 空位", accent, fg, 360, 150)
    elif layout == "root-map":
        node(d, (330, y), "根调度", accent, fg, 420, 140)
        node(d, (90, y + 280), "正确子节点", accent, fg, 400, 160)
        node(d, (590, y + 280), "错挂分支", (255, 140, 150), fg, 400, 160)
        d.line((540, y + 140, 290, y + 280), fill=accent, width=4)
        d.line((540, y + 140, 790, y + 280), fill=(255, 140, 150), width=4)
        label(d, "× 错挂", (720, y + 480), 40, (255, 140, 150))
    elif layout == "span-card":
        for i, (en, zh) in enumerate([("retrieve", "检索"), ("parse", "解析")]):
            yy = y + i * 320
            u.panel(d, (90, yy, 990, yy + 280))
            label(d, en, (150, yy + 40), 44, accent)
            label(d, zh, (150, yy + 120), 36, fg)
            label(d, "input / output / time / error", (150, yy + 190), 28, (180, 190, 210))
    elif layout == "tool-call":
        node(d, (240, y), "Tool", accent, fg, 600, 140)
        for i, text in enumerate(["name", "args", "result", "error"]):
            xx = 90 + (i % 2) * 460
            yy = y + 220 + (i // 2) * 220
            node(d, (xx, yy), text, accent, fg, 400, 160)
    elif layout == "generation-stage":
        for i, text in enumerate(["prompt", "model", "output"]):
            yy = y + i * 180
            node(d, (140, yy), text, accent, fg, 800, 140)
            if i < 2:
                d.polygon([(520, yy + 148), (560, yy + 148), (540, yy + 175)], fill=accent)
        label(d, "usage 缺失写 unknown", (260, y + 580), 36, accent)
    elif layout == "iteration":
        node(d, (90, y), "Generation 1", accent, fg, 420, 150)
        node(d, (570, y), "Tool 结果", accent, fg, 420, 150)
        node(d, (240, y + 340), "Generation 2", accent, fg, 600, 180)
        d.line((300, y + 150, 480, y + 340), fill=accent, width=3)
        d.line((780, y + 150, 600, y + 340), fill=accent, width=3)
        label(d, "两次生成独立编号", (300, y + 580), 36, fg)
    elif layout == "tree":
        node(d, (360, y), "Trace", accent, fg, 360, 120)
        node(d, (360, y + 200), "Agent", accent, fg, 360, 120)
        d.line((540, y + 120, 540, y + 200), fill=accent, width=4)
        for i, text in enumerate(["Span", "Tool", "Generation"]):
            node(d, (70 + i * 330, y + 430), text, accent, fg, 290, 140)
            d.line((540, y + 320, 215 + i * 330, y + 430), fill=accent, width=3)
        label(d, "示意树，不是真实调度", (260, y + 640), 32, fg)
    elif layout == "field-card":
        items = ["type", "name", "parentObservationId", "input / output", "status"]
        for i, item in enumerate(items):
            yy = y + i * 130
            u.panel(d, (90, yy, 990, yy + 110))
            label(d, item, (140, yy + 30), 34, fg)
            label(d, "按当前版本核对", (620, yy + 34), 24, accent, True)
    elif layout == "error-node":
        node(d, (240, y), "Trace 可展开", accent, fg, 600, 140)
        node(d, (90, y + 280), "Tool 失败", (255, 140, 150), fg, 420, 180)
        node(d, (570, y + 280), "其他节点", accent, fg, 420, 180)
        d.line((540, y + 140, 300, y + 280), fill=(255, 140, 150), width=4)
        d.line((540, y + 140, 780, y + 280), fill=accent, width=3)
        label(d, "不要只把整棵树标红", (240, y + 540), 36, fg)
    elif layout == "redaction":
        u.panel(d, (90, y + 40, 990, y + 680))
        label(d, "公开画面只留结构", (150, y + 90), 40, accent)
        for i, item in enumerate(["input 已遮罩", "output 已遮罩", "错误堆栈已遮罩"]):
            yy = y + 220 + i * 140
            label(d, item, (180, yy), 40, fg)
            d.rounded_rectangle((720, yy, 900, yy + 70), radius=12, fill=(35, 42, 55))
            label(d, "••••", (770, yy + 16), 28, (230, 235, 245))
    elif layout == "waterfall":
        for i, (name, frac) in enumerate([("retrieve", .35), ("tool", .62), ("generation", .88)]):
            yy = y + 40 + i * 200
            label(d, name, (90, yy), 36, fg)
            u.rounded(d, (90, yy + 70, 990, yy + 130), 16, (25, 32, 48))
            u.rounded(d, (90, yy + 70, 90 + int(900 * frac), yy + 130), 16, accent)
            label(d, "耗时留空", (780, yy + 145), 24, (170, 180, 205), True)
    elif layout == "orphan":
        node(d, (240, y), "Trace 树", accent, fg, 600, 180)
        node(d, (70, y + 280), "子节点", accent, fg, 300, 150)
        node(d, (400, y + 280), "子节点", accent, fg, 300, 150)
        u.panel(d, (720, y + 430, 1000, y + 650), (65, 18, 28))
        label(d, "孤立", (790, y + 480), 40, (255, 140, 150))
        label(d, "parent 空", (760, y + 560), 28, fg)
    elif layout == "duplicate":
        node(d, (90, y + 80), "同一 Tool 调用", accent, fg, 900, 150)
        node(d, (90, y + 320), "记录 A", accent, fg, 420, 180)
        u.panel(d, (570, y + 320, 990, y + 500), (65, 18, 28))
        label(d, "重复副本", (650, y + 370), 40, (255, 140, 150))
        label(d, "会污染统计", (250, y + 580), 36, fg)
    elif layout == "missing-branch":
        node(d, (330, y), "已知分支", accent, fg, 420, 150)
        for i, text in enumerate(["实线步骤", "虚线未知", "采样/漏接"]):
            xx = 70 + i * 330
            node(d, (xx, y + 300), text, accent if i == 0 else (100, 110, 135), fg, 290, 180)
        label(d, "缺口明确可见", (340, y + 560), 36, fg)
    elif layout == "readback-loop":
        for i, item in enumerate(["发出请求", "Trace ID", "树回读", "字段核对"]):
            yy = y + i * 175
            node(d, (140, yy), item, accent, fg, 800, 140)
            if i < 3:
                d.polygon([(520, yy + 148), (560, yy + 148), (540, yy + 175)], fill=accent)
    elif layout == "decision-shield":
        node(d, (240, y), "完整调用树", accent, fg, 600, 160)
        node(d, (90, y + 300), "质量门", (255, 180, 120), fg, 420, 180)
        node(d, (570, y + 300), "权限门", (255, 140, 150), fg, 420, 180)
        label(d, "两扇门尚未通过", (300, y + 560), 40, fg)
    elif layout == "stamp":
        u.panel(d, (72, y + 45, 1008, y + 710), (40, 17, 24))
        label(d, "PROTOTYPE", (135, y + 115), 68, (255, 140, 150))
        label(d, "L1 / 课程示意", (135, y + 250), 54, fg)
        for i, item in enumerate(["Agent 树写入：未证明", "同一 ID 回读：未证明", "真实调度：未证明"]):
            label(d, item, (135, y + 390 + i * 80), 34, (255, 170, 180))
    elif layout == "cta":
        u.panel(d, (72, y + 55, 1008, y + 720), tuple(int(c * .35) for c in accent))
        label(d, "下一集 / LF-11", (130, y + 115), 38, fg)
        label(d, "同一 Dataset 比较", (130, y + 270), 48, accent)
        node(d, (120, y + 480), "候选 A", accent, fg, 380, 140)
        node(d, (560, y + 480), "候选 B", accent, fg, 380, 140)
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
    video = ROOT / "langfuse/videos/LF-10-agent-tree-xiaoxiao-v3.mp4"
    base.run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
              "-i", str(concat), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
              "-b:a", "128k", "-movflags", "+faststart", str(video)])
    srt, vtt = [], ["WEBVTT", ""]
    for i, item in enumerate(timeline, start=1):
        srt += [str(i), f"{base.ts(item['start'], True)} --> {base.ts(item['end'], True)}", item["caption"], ""]
        vtt += [f"{base.ts(item['start'])} --> {base.ts(item['end'])}", item["caption"], ""]
    (ROOT / "langfuse/captions/LF-10-xiaoxiao-v3.srt").write_text("\n".join(srt), encoding="utf-8")
    (ROOT / "langfuse/captions/LF-10-xiaoxiao-v3.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (BUILD / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"video": str(video), "duration": base.duration(video), "shots": len(timeline),
                      "last_caption_end": timeline[-1]["end"]}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
