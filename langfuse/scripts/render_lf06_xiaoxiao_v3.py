#!/usr/bin/env python3
"""Render LF-06 Evaluation/Score with original-speed Xiaoxiao TTS and 20 captioned shots."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "langfuse" / "build" / "lf06-xiaoxiao-v3"
BOARD = ROOT / "langfuse" / "LF-06-shot-board-xiaoxiao.md"
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
    ("01", "钩子", "总分 90，就能上线吗？", ["90分", "失败被藏"]),
    ("02", "平均分遮罩", "平均分会掩盖关键失败", ["示意"]),
    ("03", "Score 卡", "Score 要绑定运行证据", ["Trace", "run"]),
    ("04", "评测环", "Evaluation 不只是得到一个分数", ["四步"]),
    ("05", "评分问题", "先定义评分问题，再谈分数", ["必需字段"]),
    ("06", "刻度", "范围、单位、空值规则都要先定", ["unknown"]),
    ("07", "三种方法", "人工、代码、模型评分不能混为一谈", ["human", "code", "LLM"]),
    ("08", "代码规则", "规则通过 ≠ 语义质量一定好", ["required fields"]),
    ("09", "评审校准", "模型评审也需要校准和抽查", ["抽样"]),
    ("10", "对象地图", "先确认分数到底评的是谁", ["Trace", "run"]),
    ("11", "元数据卡", "分数之外，还要留评分版本和时间", ["按当前版本核对"]),
    ("12", "写入回执", "写入 2xx ≠ Score 已回读", ["断开的桥"]),
    ("13", "回读闭环", "同一个 ID 回读分数和原始样本", ["四步"]),
    ("14", "高低分", "高低分都要抽查", ["误判", "失败"]),
    ("15", "失败树", "低分要回到失败节点和输入输出", ["示意"]),
    ("16", "对照板", "固定条件，只改一个变量再比较", ["四把锁"]),
    ("17", "分群", "总分别离开样本量和失败类型", ["样本量"]),
    ("18", "发布闸门", "有分数，不等于通过上线决策", ["关键失败"]),
    ("19", "本集边界", "示意不是评分已跑通", ["prototype / L1"]),
    ("20", "下一集", "成本、token 和延迟怎么看", ["LF-07"]),
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
    draw.text((72, 62), f"LF-06  ·  {shot['kicker']}", font=u.font(28, True), fill=accent)
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
        u.panel(d, (90, y + 40, 990, y + 430))
        label(d, "90 分", (330, y + 140), 120, accent)
        u.panel(d, (620, y + 500, 1000, y + 720), (65, 18, 28))
        label(d, "失败样本", (670, y + 560), 36, (255, 140, 150))
        label(d, "被遮挡", (700, y + 630), 30, fg)
        label(d, "角落示意，不是真实分数", (140, y + 560), 32, fg)
    elif layout == "average-mask":
        u.rounded(d, (90, y + 80, 990, y + 200), 18, (50, 80, 120))
        u.rounded(d, (90, y + 80, 780, y + 200), 18, accent)
        label(d, "平均分条", (120, y + 110), 40, fg)
        u.panel(d, (180, y + 280, 900, y + 620), (65, 18, 28))
        label(d, "关键失败", (300, y + 380), 54, (255, 140, 150))
        label(d, "示意", (460, y + 500), 36, fg)
    elif layout == "score-card":
        node(d, (330, y), "Score", accent, fg, 420, 150)
        for i, item in enumerate(["Trace", "run", "原始输出"]):
            node(d, (70 + i * 330, y + 340), item, accent, fg, 290, 160)
            d.line((540, y + 150, 215 + i * 330, y + 340), fill=accent, width=3)
        label(d, "证据线均为示意", (340, y + 580), 36, fg)
    elif layout == "evaluation-cycle":
        for i, item in enumerate(["定义", "评分", "检查", "复核"]):
            xx, yy = 90 + (i % 2) * 460, y + 40 + (i // 2) * 300
            node(d, (xx, yy), item, accent, fg, 400, 180)
        label(d, "完整过程，不只写一个数字", (200, y + 680), 36, fg)
    elif layout == "rubric":
        u.panel(d, (90, y + 40, 990, y + 680))
        label(d, "评分问题", (150, y + 120), 36, accent)
        label(d, "是否包含必需字段？", (150, y + 250), 48, fg)
        label(d, "问题不清楚，分数再精确也没用", (150, y + 430), 34, fg)
        label(d, "示例，不是真实规则", (150, y + 540), 30, (180, 190, 210))
    elif layout == "scale":
        u.rounded(d, (90, y + 80, 990, y + 180), 16, (45, 52, 70))
        for i in range(5):
            u.rounded(d, (120 + i * 170, y + 100, 250 + i * 170, y + 160), 10, accent if i < 3 else (70, 78, 98))
        node(d, (90, y + 280), "范围 / 单位", accent, fg, 420, 180)
        node(d, (570, y + 280), "unknown", (255, 140, 150), fg, 420, 180)
        label(d, "空值不能悄悄当成 0 或满分", (180, y + 540), 36, fg)
    elif layout == "three-methods":
        for i, (name, risk) in enumerate([("human", "主观差异"), ("code", "规则盲区"), ("LLM judge", "需校准")]):
            xx = 70 + i * 330
            u.panel(d, (xx, y + 40, xx + 300, y + 620))
            label(d, name, (xx + 30, y + 160), 36, accent, max_w=240)
            label(d, risk, (xx + 30, y + 360), 32, fg, max_w=240)
    elif layout == "code-rule":
        u.panel(d, (90, y + 40, 990, y + 320))
        label(d, "required fields present?", (140, y + 140), 40, accent)
        u.panel(d, (90, y + 380, 990, y + 680), (20, 24, 36))
        label(d, "语义评价：留空", (240, y + 490), 44, (180, 190, 210))
    elif layout == "judge-calibration":
        node(d, (240, y), "评审模型", accent, fg, 600, 150)
        for i in range(3):
            u.panel(d, (90 + i * 310, y + 280, 360 + i * 310, y + 520))
            label(d, f"抽样 {i + 1}", (130 + i * 310, y + 360), 36, fg)
        label(d, "抽查卡逐一翻开", (340, y + 600), 36, accent)
    elif layout == "target-map":
        node(d, (330, y + 360), "Score", accent, fg, 420, 150)
        for i, item in enumerate(["Trace", "Observation", "run"]):
            node(d, (70 + i * 330, y), item, accent, fg, 290, 150)
            d.line((215 + i * 330, y + 150, 540, y + 360), fill=accent, width=3)
        label(d, "保留实际关联标识 · 本图为示意", (160, y + 600), 32, fg)
    elif layout == "metadata-card":
        items = ["名称", "值", "数据类型", "评分方法版本", "运行时间"]
        for i, item in enumerate(items):
            yy = y + i * 130
            u.panel(d, (90, yy, 990, yy + 110))
            label(d, item, (140, yy + 30), 36, fg)
            label(d, "按当前版本核对", (620, yy + 34), 26, accent, True)
    elif layout == "response-ticket":
        node(d, (90, y + 80), "写入 2xx", accent, fg, 380, 180)
        node(d, (610, y + 80), "已回读？", (255, 140, 150), fg, 380, 180)
        d.line((470, y + 170, 520, y + 170), fill=(120, 130, 150), width=6)
        d.line((560, y + 170, 610, y + 170), fill=(120, 130, 150), width=6)
        label(d, "桥是断开的", (370, y + 360), 40, fg)
        label(d, "响应存在 ≠ 关联正确", (250, y + 500), 36, accent)
    elif layout == "readback-loop":
        for i, item in enumerate(["写入", "拿到 ID", "回读", "原始样本"]):
            yy = y + i * 175
            node(d, (140, yy), item, accent, fg, 800, 140)
            if i < 3:
                d.polygon([(520, yy + 148), (560, yy + 148), (540, yy + 175)], fill=accent)
    elif layout == "high-low-split":
        u.panel(d, (70, y + 40, 500, y + 680))
        label(d, "高分样本", (140, y + 140), 44, fg)
        label(d, "抽查误判", (150, y + 360), 36, accent)
        u.panel(d, (580, y + 40, 1010, y + 680), (40, 17, 24))
        label(d, "低分样本", (650, y + 140), 44, fg)
        label(d, "定位失败", (650, y + 360), 36, (255, 140, 150))
    elif layout == "failure-tree":
        node(d, (240, y), "低分卡", accent, fg, 600, 140)
        node(d, (90, y + 280), "失败节点", (255, 140, 150), fg, 420, 160)
        node(d, (570, y + 280), "输入 / 输出", accent, fg, 420, 160)
        d.line((540, y + 140, 300, y + 280), fill=accent, width=3)
        d.line((540, y + 140, 780, y + 280), fill=accent, width=3)
        label(d, "所有值为示意，不是真实 Trace", (180, y + 540), 32, fg)
    elif layout == "comparison-board":
        for i, (name, state) in enumerate([("数据", "锁定"), ("Prompt", "锁定"), ("模型", "锁定"), ("评分规则", "锁定"), ("候选变量", "可切换")]):
            yy = y + i * 135
            u.panel(d, (90, yy, 990, yy + 115))
            label(d, name, (140, yy + 30), 36, fg)
            label(d, state, (680, yy + 32), 32, accent if state == "可切换" else (180, 190, 210))
    elif layout == "cohort-view":
        for i, item in enumerate(["样本量", "分组结果", "失败类型"]):
            node(d, (90, y + i * 200), item, accent, fg, 900, 150)
        label(d, "总分退到最下，不能代替这些栏", (160, y + 640), 32, fg)
    elif layout == "decision-gate":
        u.panel(d, (90, y + 40, 990, y + 280))
        label(d, "高分卡", (150, y + 120), 48, fg)
        u.panel(d, (90, y + 340, 990, y + 700), (50, 28, 18))
        label(d, "发布闸门未开", (150, y + 420), 48, (255, 180, 120))
        label(d, "预设标准 · 关键失败", (150, y + 540), 36, fg)
    elif layout == "stamp":
        u.panel(d, (72, y + 45, 1008, y + 710), (40, 17, 24))
        label(d, "PROTOTYPE", (135, y + 115), 68, (255, 140, 150))
        label(d, "L1 / 课程示意", (135, y + 250), 54, fg)
        for i, item in enumerate(["Score 写入：未证明", "Dataset run：未证明", "同 ID 回读：未证明"]):
            label(d, item, (135, y + 390 + i * 80), 34, (255, 170, 180))
    elif layout == "cta":
        u.panel(d, (72, y + 55, 1008, y + 720), tuple(int(c * .35) for c in accent))
        label(d, "下一集 / LF-07", (130, y + 115), 38, fg)
        label(d, "cost / token / latency", (130, y + 270), 48, accent)
        label(d, "字段从哪里来", (130, y + 430), 44, fg)
        label(d, "为什么不能只看一个总数？", (130, y + 540), 36, fg)
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
    video = ROOT / "langfuse/videos/LF-06-score-xiaoxiao-v3.mp4"
    base.run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
              "-i", str(concat), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
              "-b:a", "128k", "-movflags", "+faststart", str(video)])
    srt, vtt = [], ["WEBVTT", ""]
    for i, item in enumerate(timeline, start=1):
        srt += [str(i), f"{base.ts(item['start'], True)} --> {base.ts(item['end'], True)}", item["caption"], ""]
        vtt += [f"{base.ts(item['start'])} --> {base.ts(item['end'])}", item["caption"], ""]
    (ROOT / "langfuse/captions/LF-06-xiaoxiao-v3.srt").write_text("\n".join(srt), encoding="utf-8")
    (ROOT / "langfuse/captions/LF-06-xiaoxiao-v3.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (BUILD / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"video": str(video), "duration": base.duration(video), "shots": len(timeline),
                      "last_caption_end": timeline[-1]["end"]}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
