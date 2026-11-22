#!/usr/bin/env python3
"""Render LF-08 user-feedback loop with original-speed Xiaoxiao and burned captions."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "langfuse/build/lf08-xiaoxiao-v3"
BOARD = ROOT / "langfuse/LF-08-shot-board-xiaoxiao.md"
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
    ("01", "钩子", "一条点踩，不能代表所有用户", ["点踩", "满意度留空"]),
    ("02", "单条事件", "反馈先是一条具体事件", ["类型", "时间"]),
    ("03", "关联 Trace", "把反馈和原始 Trace 对上", ["占位符"]),
    ("04", "上下文卡", "反馈要带上运行版本和上下文", ["版本", "时间"]),
    ("05", "类型网格", "点赞、评分、评论不是同一种数据", ["thumbs", "rating", "comment"]),
    ("06", "量表", "先定义取值范围，再比较分数", ["1-5", "另一套"]),
    ("07", "评论分流", "没有标签的评论，不直接当分数", ["人工", "文本"]),
    ("08", "空值盒", "没有反馈 ≠ 满意或零分", ["unknown"]),
    ("09", "来源泳道", "反馈来源不同，不能不加区分地混算", ["user", "human", "model"]),
    ("10", "绑定地图", "反馈要绑定到正确的运行对象", ["按当前版本核对"]),
    ("11", "回读闭环", "同一个 ID 回读反馈和原始记录", ["四步"]),
    ("12", "写入回执", "写入 2xx ≠ 反馈回读成功", ["三件事"]),
    ("13", "正负空值", "好评、差评和空值都要抽查", ["抽样"]),
    ("14", "沉默多数", "没反馈的人，不一定都满意", ["少数发言"]),
    ("15", "分母", "反馈百分比必须带分母和采样范围", ["数值留空"]),
    ("16", "脱敏", "评论原文先脱敏，再进入样本库", ["权限"]),
    ("17", "回流 Dataset", "反馈样本审核后再进入 Dataset", ["source", "version"]),
    ("18", "回归看板", "进入 Dataset ≠ 问题已修复", ["待实测"]),
    ("19", "本集边界", "不是反馈已回流", ["prototype / L1"]),
    ("20", "下一集", "采样、脱敏和保留策略", ["LF-09"]),
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
    draw.text((72, 62), f"LF-08  ·  {shot['kicker']}", font=u.font(28, True), fill=accent)
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
        node(d, (90, y + 40), "点踩", (255, 140, 150), fg, 320, 220)
        u.panel(d, (470, y + 80, 980, y + 260))
        label(d, "单条反馈卡", (520, y + 130), 40, fg)
        u.panel(d, (90, y + 360, 980, y + 680))
        label(d, "整体满意度", (150, y + 430), 40, fg)
        label(d, "仪表留空 / 示意", (150, y + 530), 36, accent)
    elif layout == "single-event":
        u.panel(d, (90, y + 40, 990, y + 680))
        for i, (k, v) in enumerate([("反馈类型", "thumbs-down 示意"), ("时间", "录制当天"), ("上下文", "已脱敏")]):
            yy = y + 90 + i * 170
            label(d, k, (150, yy), 34, accent)
            label(d, v, (150, yy + 70), 40, fg)
    elif layout == "trace-link":
        node(d, (330, y), "反馈卡", accent, fg, 420, 150)
        for i, item in enumerate(["Trace", "input", "output"]):
            node(d, (70 + i * 330, y + 340), item, accent, fg, 290, 160)
            d.line((540, y + 150, 215 + i * 330, y + 340), fill=accent, width=3)
        label(d, "ID 使用占位符", (340, y + 580), 36, fg)
    elif layout == "context-card":
        for i, item in enumerate(["版本", "运行时间", "Trace ID", "不含用户原文"]):
            yy = y + i * 165
            u.panel(d, (90, yy, 990, yy + 140))
            label(d, item, (150, yy + 40), 40, fg)
            label(d, "示意", (780, yy + 48), 28, accent)
    elif layout == "type-grid":
        for i, (name, note) in enumerate([("thumbs", "点赞/点踩"), ("rating", "数值评分"), ("comment", "文字评论")]):
            xx = 70 + i * 330
            u.panel(d, (xx, y + 40, xx + 300, y + 620))
            label(d, name, (xx + 30, y + 160), 36, accent, max_w=240)
            label(d, note, (xx + 30, y + 360), 32, fg, max_w=240)
            label(d, "不混用", (xx + 70, y + 500), 30, (180, 190, 210))
    elif layout == "scale":
        u.panel(d, (70, y + 40, 500, y + 680))
        label(d, "产品 A", (140, y + 90), 36, accent)
        label(d, "1 - 5", (150, y + 280), 54, fg)
        u.panel(d, (580, y + 40, 1010, y + 680))
        label(d, "产品 B", (650, y + 90), 36, accent)
        label(d, "另一套量表", (620, y + 280), 40, fg)
        label(d, "不能直接混算", (300, y + 720), 32, (255, 160, 170))
    elif layout == "comment-split":
        node(d, (240, y), "无标签评论", accent, fg, 600, 150)
        node(d, (90, y + 300), "人工规则", accent, fg, 400, 180)
        node(d, (590, y + 300), "文本分析", accent, fg, 400, 180)
        d.line((540, y + 150, 290, y + 300), fill=accent, width=3)
        d.line((540, y + 150, 790, y + 300), fill=accent, width=3)
        label(d, "禁止自动数值化", (300, y + 560), 40, (255, 140, 150))
    elif layout == "null-box":
        node(d, (90, y + 40), "好评", accent, fg, 280, 160)
        node(d, (400, y + 40), "差评", (255, 140, 150), fg, 280, 160)
        u.panel(d, (180, y + 320, 900, y + 640), (20, 24, 36))
        label(d, "unknown", (360, y + 380), 54, accent)
        label(d, "未反馈样本单独处理", (250, y + 500), 36, fg)
    elif layout == "source-lanes":
        for i, name in enumerate(["user", "human", "model"]):
            yy = y + i * 210
            u.panel(d, (90, yy, 990, yy + 180))
            label(d, name, (140, yy + 55), 44, accent)
            label(d, "汇总前先分组", (520, yy + 62), 32, fg)
    elif layout == "binding-map":
        node(d, (90, y + 80), "feedback", accent, fg, 360, 180)
        node(d, (630, y + 40), "Trace", accent, fg, 360, 150)
        node(d, (630, y + 260), "Observation", accent, fg, 360, 150)
        d.line((450, y + 170, 630, y + 115), fill=accent, width=3)
        d.line((450, y + 170, 630, y + 335), fill=accent, width=3)
        label(d, "字段按当前版本核对", (220, y + 500), 36, fg)
    elif layout == "readback-loop":
        for i, item in enumerate(["写入", "关联 ID", "同一条回读", "原始记录"]):
            yy = y + i * 175
            node(d, (140, yy), item, accent, fg, 800, 140)
            if i < 3:
                d.polygon([(520, yy + 148), (560, yy + 148), (540, yy + 175)], fill=accent)
    elif layout == "response-ticket":
        for i, (name, note) in enumerate([("写入 2xx", "响应存在"), ("关联正确?", "待核对"), ("已回读?", "未证明")]):
            xx = 70 + i * 330
            u.panel(d, (xx, y + 80, xx + 300, y + 520))
            label(d, name, (xx + 24, y + 180), 32, accent, max_w=250)
            label(d, note, (xx + 40, y + 340), 32, fg, max_w=230)
        label(d, "三件事不能互相替代", (260, y + 620), 36, fg)
    elif layout == "pos-neg":
        for i, (name, color) in enumerate([("正例", accent), ("负例", (255, 140, 150)), ("空值", (180, 190, 210))]):
            xx = 70 + i * 330
            u.panel(d, (xx, y + 40, xx + 300, y + 620))
            label(d, name, (xx + 70, y + 160), 40, color)
            label(d, "抽样卡", (xx + 70, y + 360), 32, fg)
    elif layout == "silent-majority":
        for r in range(3):
            for c in range(4):
                x, yy = 90 + c * 240, y + 20 + r * 130
                u.panel(d, (x, yy, x + 210, yy + 100), (24, 30, 44))
        u.panel(d, (90, y + 460, 420, y + 680))
        label(d, "少数发言", (140, y + 530), 36, accent)
        label(d, "沉默多数仍是轮廓", (430, y + 540), 32, fg)
    elif layout == "denominator":
        u.panel(d, (90, y + 40, 990, y + 280))
        label(d, "百分比", (150, y + 120), 54, fg)
        label(d, "数值留空", (620, y + 140), 36, accent)
        node(d, (90, y + 360), "分母", accent, fg, 420, 220)
        node(d, (570, y + 360), "采样范围", accent, fg, 420, 220)
    elif layout == "redaction":
        node(d, (90, y + 40), "评论原文", (255, 140, 150), fg, 360, 180)
        node(d, (360, y + 300), "脱敏遮罩", accent, fg, 360, 160)
        node(d, (630, y + 500), "受权限样本库", accent, fg, 360, 160)
        d.line((270, y + 220, 430, y + 300), fill=accent, width=4)
        d.line((540, y + 460, 720, y + 500), fill=accent, width=4)
        label(d, "公开画面不含原文", (220, y + 700), 32, fg)
    elif layout == "dataset-return":
        node(d, (240, y), "审核后的反馈", accent, fg, 600, 150)
        node(d, (90, y + 300), "source", accent, fg, 420, 180)
        node(d, (570, y + 300), "version", accent, fg, 420, 180)
        node(d, (240, y + 540), "Dataset", accent, fg, 600, 140)
        d.line((540, y + 150, 300, y + 300), fill=accent, width=3)
        d.line((540, y + 150, 780, y + 300), fill=accent, width=3)
        d.line((300, y + 480, 420, y + 540), fill=accent, width=3)
        d.line((780, y + 480, 660, y + 540), fill=accent, width=3)
    elif layout == "regression-board":
        for i, item in enumerate(["旧版本", "新版本", "同一失败样本"]):
            yy = y + i * 200
            u.panel(d, (90, yy, 990, yy + 170))
            label(d, item, (150, yy + 30), 40, fg)
            label(d, "结果待实测", (620, yy + 40), 32, accent)
    elif layout == "stamp":
        u.panel(d, (72, y + 45, 1008, y + 710), (40, 17, 24))
        label(d, "PROTOTYPE", (135, y + 115), 68, (255, 140, 150))
        label(d, "L1 / 课程示意", (135, y + 250), 54, fg)
        for i, item in enumerate(["收到反馈：未证明", "Score 写入：未证明", "同 ID 回读：未证明"]):
            label(d, item, (135, y + 390 + i * 80), 34, (255, 170, 180))
    elif layout == "cta":
        u.panel(d, (72, y + 55, 1008, y + 720), tuple(int(c * .35) for c in accent))
        label(d, "下一集 / LF-09", (130, y + 115), 38, fg)
        label(d, "采样 / 脱敏 / 保留", (130, y + 270), 48, accent)
        for i, text in enumerate(["采样率", "脱敏", "保留期限"]):
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
    video = ROOT / "langfuse/videos/LF-08-feedback-xiaoxiao-v3.mp4"
    base.run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
              "-i", str(concat), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
              "-b:a", "128k", "-movflags", "+faststart", str(video)])
    srt, vtt = [], ["WEBVTT", ""]
    for i, item in enumerate(timeline, start=1):
        srt += [str(i), f"{base.ts(item['start'], True)} --> {base.ts(item['end'], True)}", item["caption"], ""]
        vtt += [f"{base.ts(item['start'])} --> {base.ts(item['end'])}", item["caption"], ""]
    (ROOT / "langfuse/captions/LF-08-xiaoxiao-v3.srt").write_text("\n".join(srt), encoding="utf-8")
    (ROOT / "langfuse/captions/LF-08-xiaoxiao-v3.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (BUILD / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"video": str(video), "duration": base.duration(video), "shots": len(timeline),
                      "last_caption_end": timeline[-1]["end"]}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
