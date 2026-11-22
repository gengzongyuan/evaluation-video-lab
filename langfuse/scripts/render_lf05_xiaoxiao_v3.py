#!/usr/bin/env python3
"""Render LF-05 Dataset with original-speed Xiaoxiao TTS and 20 captioned shots."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "langfuse" / "build" / "lf05-xiaoxiao-v3"
BOARD = ROOT / "langfuse" / "LF-05-shot-board-xiaoxiao.md"
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
    ("01", "钩子", "换题了，还是真的变好了？", ["样例", "可重复"]),
    ("02", "单条样例", "单条样例解释不了整体", ["失败面被挡住"]),
    ("03", "Dataset 卡", "让实验回到同一组题", ["示意名"]),
    ("04", "item 网格", "每条样本都有输入和参考", ["脱敏"]),
    ("05", "稳定标识", "结果要能追回原来的 item", ["item_demo_01"]),
    ("06", "三栏对照", "期望结果不能覆盖实际输出", ["input", "expected", "actual"]),
    ("07", "冻结板", "先冻结数据和运行条件", ["五块锁定"]),
    ("08", "第一次 run", "保存原始输出和关联记录", ["Prompt v1"]),
    ("09", "单变量", "只改一个变量", ["其余锁定"]),
    ("10", "第二次 run", "仍用同一 Dataset", ["Prompt v2"]),
    ("11", "逐条对照", "先逐条对照，再看汇总", ["失败类别"]),
    ("12", "失败样本", "平均分会掩盖回退", ["关键样本"]),
    ("13", "Score 附着", "分数要追到规则和对象", ["示意连线"]),
    ("14", "run 元数据", "把这次条件完整留下", ["脱敏占位"]),
    ("15", "Trace 回看", "低分背后要有 Trace", ["中间步骤"]),
    ("16", "回读闭环", "回读同一轮 Dataset / run / Score", ["四步"]),
    ("17", "证据门", "health 200 ≠ 实验已完成", ["BLOCKED"]),
    ("18", "代表性", "固定样本 ≠ 样本有代表性", ["覆盖待评估"]),
    ("19", "本集边界", "示意不是实验已跑通", ["prototype / L1"]),
    ("20", "下一集", "有了分数，能否直接上线？", ["LF-06"]),
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
    draw.text((72, 62), f"LF-05  ·  {shot['kicker']}", font=u.font(28, True), fill=accent)
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
        u.panel(d, (70, y + 40, 500, y + 520))
        u.panel(d, (580, y + 40, 1010, y + 520))
        label(d, "简单题", (160, y + 120), 40, accent)
        label(d, "变好了?", (160, y + 280), 44, fg)
        label(d, "难题", (720, y + 120), 40, accent)
        label(d, "换题了", (690, y + 280), 44, (255, 140, 150))
        label(d, "换题了？", (390, y + 620), 54, accent)
    elif layout == "two-demo":
        u.panel(d, (70, y + 40, 620, y + 680))
        label(d, "单条高分样例", (130, y + 140), 44, fg)
        label(d, "放大展示", (130, y + 280), 36, accent)
        u.panel(d, (680, y + 40, 1010, y + 680), (18, 20, 28))
        label(d, "失败样本", (730, y + 250), 36, (150, 155, 170))
        label(d, "被挡住", (755, y + 360), 36, (150, 155, 170))
    elif layout == "dataset-card":
        u.panel(d, (90, y + 30, 990, y + 700), (240, 244, 248))
        label(d, "DATASET", (150, y + 80), 32, (25, 50, 75))
        label(d, "intro-demo-v1", (150, y + 160), 48, (30, 45, 65))
        for i, text in enumerate(["item A", "item B", "item C"]):
            node(d, (150 + i * 270, y + 320), text, (35, 120, 105), (30, 45, 65), 230, 140)
        label(d, "示意名 · 不是当前项目已创建", (150, y + 560), 30, (90, 100, 120))
    elif layout == "item-grid":
        headers = ["input", "expected_output", "metadata"]
        for i, h in enumerate(headers):
            label(d, h, (90 + i * 330, y + 20), 30, accent, True, 280)
        for r in range(3):
            for c in range(3):
                u.panel(d, (70 + c * 330, y + 90 + r * 200, 370 + c * 330, y + 250 + r * 200))
                label(d, "脱敏占位", (95 + c * 330, y + 140 + r * 200), 28, fg, True, 240)
    elif layout == "id-tag":
        u.panel(d, (90, y + 80, 990, y + 360))
        label(d, "item_demo_01", (150, y + 160), 56, accent)
        label(d, "示意 ID · 禁止伪造真实样本", (150, y + 260), 30, fg)
        node(d, (90, y + 460), "来源", accent, fg, 400, 160)
        node(d, (590, y + 460), "版本", accent, fg, 400, 160)
    elif layout == "input-output":
        for i, text in enumerate(["input", "expected", "actual"]):
            node(d, (90, y + 40 + i * 220), text, accent, fg, 900, 160)
        label(d, "actual 独立存放，不被 expected 覆盖", (160, y + 720), 34, accent)
    elif layout == "freeze-board":
        for i, text in enumerate(["Dataset", "Prompt", "模型", "参数", "评分规则"]):
            xx, yy = 70 + (i % 3) * 330, y + 40 + (i // 3) * 320
            u.panel(d, (xx, yy, xx + 300, yy + 250))
            label(d, "锁定", (xx + 90, yy + 60), 28, accent)
            label(d, text, (xx + 40, yy + 130), 36, fg, max_w=230)
    elif layout == "run-first":
        node(d, (240, y), "Prompt v1 / run 1", accent, fg, 600, 140)
        for i, text in enumerate(["item A", "item B", "item C"]):
            node(d, (90 + i * 310, y + 280), text, accent, fg, 270, 140)
            d.line((540, y + 140, 225 + i * 310, y + 280), fill=accent, width=3)
        u.panel(d, (90, y + 500, 990, y + 680))
        label(d, "原始输出抽屉 · 示意空值", (220, y + 555), 36, fg)
    elif layout == "single-variable":
        for i, (name, state) in enumerate([("Prompt", "v1 -> v2"), ("模型", "锁定"), ("参数", "锁定"), ("数据", "锁定"), ("评分规则", "锁定")]):
            yy = y + i * 135
            u.panel(d, (90, yy, 990, yy + 115))
            label(d, name, (140, yy + 30), 36, fg)
            label(d, state, (680, yy + 32), 32, accent if "v1" in state else (180, 190, 210))
    elif layout == "run-second":
        node(d, (90, y + 40), "Dataset 同一组题", accent, fg, 900, 140)
        node(d, (90, y + 280), "run 1 / Prompt v1", accent, fg, 420, 180)
        node(d, (570, y + 280), "run 2 / Prompt v2", accent, fg, 420, 180)
        d.line((540, y + 180, 300, y + 280), fill=accent, width=4)
        d.line((540, y + 180, 780, y + 280), fill=accent, width=4)
        label(d, "两次运行保留各自条件和时间", (180, y + 560), 36, fg)
    elif layout == "comparison-table":
        heads = ["item", "v1", "v2", "失败类别"]
        for i, h in enumerate(heads):
            label(d, h, (90 + i * 240, y + 20), 28, accent, True, 200)
        for r in range(4):
            for c in range(4):
                u.panel(d, (70 + c * 245, y + 90 + r * 150, 290 + c * 245, y + 210 + r * 150))
                label(d, "示意", (110 + c * 245, y + 125 + r * 150), 28, fg, True)
    elif layout == "failure-focus":
        u.panel(d, (90, y + 40, 520, y + 280), (20, 24, 36))
        label(d, "平均分", (170, y + 120), 44, (160, 170, 190))
        u.panel(d, (180, y + 320, 990, y + 700), (65, 18, 28))
        label(d, "关键失败样本", (240, y + 420), 54, (255, 140, 150))
        label(d, "必须单独展开", (240, y + 530), 40, fg)
    elif layout == "score-attachment":
        node(d, (360, y), "Score", accent, fg, 360, 130)
        for i, text in enumerate(["item", "run", "evaluator"]):
            node(d, (90 + i * 310, y + 320), text, accent, fg, 270, 150)
            d.line((540, y + 130, 225 + i * 310, y + 320), fill=accent, width=3)
        label(d, "连线均为示意", (370, y + 560), 36, fg)
    elif layout == "run-metadata":
        items = ["Dataset 版本", "Prompt", "模型", "参数", "代码版本", "运行时间"]
        for i, text in enumerate(items):
            xx, yy = 70 + (i % 2) * 480, y + 20 + (i // 2) * 230
            u.panel(d, (xx, yy, xx + 440, yy + 190))
            label(d, text, (xx + 40, yy + 40), 36, fg)
            label(d, "脱敏占位", (xx + 40, yy + 105), 28, accent, True)
    elif layout == "trace-link":
        for i, text in enumerate(["失败 item", "run item", "Trace 树"]):
            node(d, (140, y + i * 210), text, accent, fg, 800, 150)
            if i < 2:
                d.polygon([(520, y + 163 + i * 210), (560, y + 163 + i * 210), (540, y + 198 + i * 210)], fill=accent)
        label(d, "低分卡只占一角，不是全部证据", (200, y + 680), 34, accent)
    elif layout == "readback-loop":
        for i, text in enumerate(["写入", "拿到标识", "回读", "核对关系"]):
            yy = y + i * 175
            node(d, (140, yy), text, accent, fg, 800, 140)
            if i < 3:
                d.polygon([(520, yy + 148), (560, yy + 148), (540, yy + 175)], fill=accent)
    elif layout == "boundary-gate":
        u.panel(d, (120, y + 20, 960, y + 220), (65, 18, 28))
        label(d, "BLOCKED", (360, y + 80), 64, (255, 125, 135))
        node(d, (90, y + 320), "health 200", accent, fg, 400, 160)
        node(d, (590, y + 320), "UI 截图", accent, fg, 400, 160)
        label(d, "真实 run 区留白", (330, y + 560), 40, fg)
    elif layout == "representativeness":
        for i in range(3):
            d.ellipse((160 + i * 120, y + 80, 220 + i * 120, y + 140), fill=accent)
        d.rounded_rectangle((90, y + 250, 990, y + 620), radius=28, outline=(90, 100, 125), width=3)
        label(d, "业务分布未覆盖", (250, y + 390), 48, fg)
        label(d, "覆盖仍待评估", (320, y + 700), 38, (255, 140, 150))
    elif layout == "stamp":
        u.panel(d, (72, y + 45, 1008, y + 710), (40, 17, 24))
        label(d, "PROTOTYPE", (135, y + 115), 68, (255, 140, 150))
        label(d, "L1 / 课程示意", (135, y + 250), 54, fg)
        for i, text in enumerate(["Dataset 写入：未证明", "run / Score：未证明", "实验回读：未证明"]):
            label(d, text, (135, y + 390 + i * 80), 34, (255, 170, 180))
    elif layout == "cta":
        u.panel(d, (72, y + 55, 1008, y + 720), tuple(int(c * .35) for c in accent))
        label(d, "下一集 / LF-06", (130, y + 115), 38, fg)
        label(d, "Evaluation / Score", (130, y + 270), 54, accent)
        label(d, "有了分数", (130, y + 430), 48, fg)
        label(d, "为什么仍不能直接上线？", (130, y + 540), 40, fg)
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
    video = ROOT / "langfuse/videos/LF-05-dataset-xiaoxiao-v3.mp4"
    base.run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
              "-i", str(concat), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
              "-b:a", "128k", "-movflags", "+faststart", str(video)])
    srt, vtt = [], ["WEBVTT", ""]
    for i, item in enumerate(timeline, start=1):
        srt += [str(i), f"{base.ts(item['start'], True)} --> {base.ts(item['end'], True)}", item["caption"], ""]
        vtt += [f"{base.ts(item['start'])} --> {base.ts(item['end'])}", item["caption"], ""]
    (ROOT / "langfuse/captions/LF-05-xiaoxiao-v3.srt").write_text("\n".join(srt), encoding="utf-8")
    (ROOT / "langfuse/captions/LF-05-xiaoxiao-v3.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (BUILD / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"video": str(video), "duration": base.duration(video), "shots": len(timeline),
                      "last_caption_end": timeline[-1]["end"]}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
