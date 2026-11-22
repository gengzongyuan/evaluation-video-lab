#!/usr/bin/env python3
"""Render LF-07 with original-speed Xiaoxiao TTS and 20 captioned shots.

The narration and captions are read directly from the approved shot board.
All identifiers and diagrams are explicitly marked as course demonstrations.
"""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "langfuse" / "build" / "lf07-xiaoxiao-v3"
BOARD = ROOT / "langfuse" / "LF-07-shot-board-xiaoxiao.md"
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
    ("01", "钩子", "回答慢，就是模型慢？", ["总等待", "分段定位"]),
    ("02", "完整链路", "先拆链路，再看总耗时", ["请求时间线"]),
    ("03", "Generation · 模型调用", "模型调用单独看", ["model", "start / end"]),
    ("04", "token usage · 用量", "输入和输出分开看", ["input", "output"]),
    ("05", "usage 字段", "更细的字段，看实际返回", ["provider / SDK", "unknown"]),
    ("06", "缺失字段", "缺 usage，不猜", ["unknown", "禁止补数"]),
    ("07", "成本条件", "金额不是凭空算出来的", ["usage", "price config"]),
    ("08", "价格配置", "价格快照不是账单", ["来源", "币种", "版本 / 日期"]),
    ("09", "证据边界", "用量和质量是两条证据", ["token", "quality"]),
    ("10", "latency · 延迟", "先说清起止点和时区", ["start", "end", "timezone"]),
    ("11", "耗时瀑布", "时间到底花在哪里？", ["结构示意", "非实测"]),
    ("12", "多样本证据", "一次调用推不出 P95", ["P95", "SLA", "多样本"]),
    ("13", "对照条件", "固定条件，只改一个变量", ["控制变量"]),
    ("14", "原始记录", "先保存原始字段，再汇总", ["脱敏", "raw fields"]),
    ("15", "A / B 对照", "每一轮都能追回去", ["run 占位", "同一输入"]),
    ("16", "验收闭环", "同一条 Generation 回读", ["同一 ID", "字段核对"]),
    ("17", "证据门", "证据不够，就保持 BLOCKED", ["BLOCKED"]),
    ("18", "优化边界", "成本、速度和质量一起看", ["质量门", "失败样本"]),
    ("19", "本集边界", "示意不是实测", ["prototype / L1"]),
    ("20", "下一集", "用户反馈怎样回到 Score？", ["LF-08", "Score"]),
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
    rows = {}
    pattern = re.compile(
        r"^\| (\d{2}) \| `([^`]+)` \| [^|]+ \| (.*?) \| (.*?) \| (.*?) \|$",
        re.M,
    )
    for match in pattern.finditer(BOARD.read_text(encoding="utf-8")):
        sid, layout, voice, _visual, caption = match.groups()
        rows[sid] = dict(id=sid, layout=layout, voice=voice, caption=caption)
    shots = []
    for sid, kicker, title, chips in META:
        shot = rows[sid]
        shot.update(kicker=kicker, title=title, chips=chips)
        shots.append(shot)
    if len(shots) != 20 or len({s['layout'] for s in shots}) != 20:
        raise ValueError("expected 20 shots with 20 unique layouts")
    return shots


SHOTS = load_shots()


def label(draw, text, xy, size=32, color=(237, 244, 255), light=False, max_w=880):
    return base.label(draw, text, xy, size, color, light, max_w)


def header(draw, shot, idx, accent, fg):
    draw.text((72, 62), f"LF-07  ·  {shot['kicker']}", font=u.font(28, True), fill=accent)
    label(draw, shot["title"], (72, 118), 54, fg, max_w=930)
    draw.text((72, 252), f"{idx:02d} / 20    prototype / L1", font=u.font(24, True), fill=(185, 195, 215))
    u.rounded(draw, (72, 304, 1008, 314), 5, (41, 48, 65))
    u.rounded(draw, (72, 304, 72 + int(936 * idx / 20), 314), 5, accent)


def node(draw, xy, text, accent, fg, width=260, height=140):
    base.node(draw, xy, text, accent, fg, width, height)


def field_rows(draw, rows, y, accent, fg, value="unknown"):
    for i, name in enumerate(rows):
        yy = y + i * 122
        u.panel(draw, (90, yy, 990, yy + 94), (9, 14, 26))
        label(draw, name, (125, yy + 23), 34, fg)
        label(draw, value, (710, yy + 26), 28, accent, True, max_w=240)


def draw_shot(shot, idx):
    bg, accent, fg = PALETTES[(idx - 1) % len(PALETTES)]
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    header(d, shot, idx, accent, fg)
    y = 380
    layout = shot["layout"]
    if layout == "hook":
        label(d, "慢", (390, y + 20), 220, accent)
        label(d, "总等待", (425, y + 275), 44, fg)
        for i, text in enumerate(["检索 ?", "工具 ?", "模型 ?"]):
            node(d, (70 + i * 315, y + 430), text, accent, fg, 290, 155)
        label(d, "先拆开，再下结论", (275, y + 690), 42, fg)
    elif layout == "pipeline":
        for i, text in enumerate(["请求", "检索", "工具", "模型", "答案"]):
            xx = 52 + i * 202
            node(d, (xx, y + 230), text, accent, fg, 170, 160)
            if i < 4:
                base.arrow(d, (xx + 174, y + 310), (xx + 197, y + 310), accent)
        label(d, "每一段时间都归每一段", (205, y + 540), 42, fg)
        label(d, "总耗时 = 完整链路", (300, y + 630), 38, accent)
    elif layout == "generation-window":
        u.panel(d, (72, y + 20, 1008, y + 735), (8, 13, 25))
        label(d, "GENERATION", (120, y + 65), 42, accent)
        field_rows(d, ["model / 模型", "start / 开始", "end / 结束", "input / output"], y + 150, accent, fg, "看原始字段")
    elif layout == "token-bar":
        label(d, "token usage", (72, y + 40), 48, accent)
        u.rounded(d, (72, y + 180, 540, y + 350), 28, (39, 93, 140))
        u.rounded(d, (540, y + 180, 1008, y + 350), 28, (110, 75, 155))
        label(d, "input / 输入", (160, y + 225), 42, fg)
        label(d, "output / 输出", (625, y + 225), 42, fg)
        label(d, "结构示意 · 不填虚构数量", (220, y + 440), 38, fg)
        label(d, "保留原始字段，再解释总量", (195, y + 560), 38, accent)
    elif layout == "nested-usage":
        node(d, (340, y), "usage", accent, fg, 400, 130)
        for i, text in enumerate(["input", "output", "cache", "reasoning"]):
            xx = 45 + i * 245
            node(d, (xx, y + 330), text, accent, fg, 215, 130)
            label(d, "unknown", (xx + 30, y + 500), 26, (175, 185, 205), True, 180)
            d.line((540, y + 130, xx + 107, y + 330), fill=(105, 115, 145), width=3)
        label(d, "以 provider / SDK 实际返回为准", (145, y + 680), 38, accent)
    elif layout == "unknown-stamp":
        u.panel(d, (90, y + 40, 990, y + 390), (240, 244, 248))
        label(d, "usage", (150, y + 105), 50, (30, 45, 65))
        label(d, "unknown", (150, y + 215), 88, (185, 55, 75))
        u.panel(d, (90, y + 475, 990, y + 690), (10, 14, 25))
        label(d, "字符数  →  token", (180, y + 530), 50, fg)
        d.line((150, y + 500, 930, y + 665), fill=(255, 100, 115), width=16)
        label(d, "不能估算后冒充真实消耗", (215, y + 745), 36, accent)
    elif layout == "cost-equation":
        label(d, "成本", (110, y + 120), 64, fg)
        label(d, "=", (310, y + 120), 64, accent)
        node(d, (410, y + 65), "usage", accent, fg, 250, 160)
        label(d, "×", (695, y + 120), 60, accent)
        node(d, (770, y + 65), "价格配置", accent, fg, 250, 160)
        u.panel(d, (110, y + 355, 970, y + 510), (9, 14, 26))
        label(d, "+ 明确的计价时间", (250, y + 405), 44, fg)
        label(d, "缺一项，就不能给确定金额", (180, y + 650), 40, accent)
    elif layout == "price-card":
        u.panel(d, (90, y + 30, 990, y + 710), (240, 244, 248))
        label(d, "PRICE CONFIG / 配置快照", (140, y + 80), 38, (25, 50, 75))
        for i, text in enumerate(["来源 source", "币种 currency", "版本 version", "日期 date"]):
            yy = y + 190 + i * 115
            label(d, text, (150, yy), 36, (30, 45, 65))
            label(d, "需记录", (730, yy), 30, (35, 120, 105))
        label(d, "≠ 本次真实账单", (285, y + 770), 46, accent)
    elif layout == "volume-compare":
        u.panel(d, (60, y + 50, 490, y + 650), (9, 14, 26))
        u.panel(d, (590, y + 50, 1020, y + 650), (9, 14, 26))
        label(d, "token 用量", (140, y + 105), 42, accent)
        for i, width in enumerate([220, 300, 160]):
            u.rounded(d, (115, y + 235 + i * 90, 115 + width, y + 270 + i * 90), 12, accent)
        label(d, "回答质量", (670, y + 105), 42, accent)
        label(d, "需独立评估", (675, y + 285), 38, fg)
        label(d, "两条证据", (725, y + 420), 34, fg)
        label(d, "不画因果箭头", (390, y + 735), 36, accent)
    elif layout == "timestamp":
        node(d, (90, y + 90), "start_time", accent, fg, 400, 170)
        node(d, (590, y + 90), "end_time", accent, fg, 400, 170)
        label(d, "同一事件", (180, y + 320), 36, fg)
        label(d, "end − start = latency", (195, y + 450), 54, accent)
        u.panel(d, (90, y + 590, 990, y + 735), (9, 14, 26))
        label(d, "时区 timezone：必须写清", (210, y + 635), 40, fg)
    elif layout == "waterfall":
        for i, (name, width) in enumerate([("检索", 300), ("工具", 410), ("排队", 260), ("模型", 500)]):
            yy = y + 30 + i * 175
            label(d, name, (75, yy), 36, fg)
            u.rounded(d, (250, yy, 250 + width, yy + 70), 18, accent if i != 2 else (160, 145, 190))
            label(d, "示意", (800, yy + 12), 28, (180, 190, 210), True)
        label(d, "区间无数值 · 不是实测", (265, y + 750), 36, accent)
    elif layout == "trend-blank":
        u.panel(d, (65, y + 40, 425, y + 650), (9, 14, 26))
        label(d, "单次调用", (125, y + 90), 40, fg)
        d.ellipse((210, y + 300, 280, y + 370), fill=accent)
        label(d, "只说明这一次", (100, y + 500), 32, accent)
        u.panel(d, (520, y + 40, 1015, y + 650), (9, 14, 26))
        label(d, "P95 / SLA", (625, y + 90), 40, fg)
        d.rectangle((590, y + 200, 945, y + 475), outline=(90, 100, 125), width=3)
        label(d, "无多样本证据", (610, y + 530), 34, (255, 125, 135))
        label(d, "不能由单条 Trace 推出来", (220, y + 740), 38, accent)
    elif layout == "control-board":
        for i, text in enumerate(["输入", "模型", "参数", "网络", "样本"]):
            xx = 50 + i * 198
            u.panel(d, (xx, y + 80, xx + 175, y + 310), (9, 14, 26))
            label(d, "锁定", (xx + 45, y + 115), 30, accent)
            label(d, text, (xx + 48, y + 205), 38, fg)
        base.arrow(d, (540, y + 360), (540, y + 450), accent)
        u.panel(d, (150, y + 480, 930, y + 680), tuple(int(c * .35) for c in accent))
        label(d, "只改一个条件", (320, y + 535), 54, fg)
        label(d, "其他条件保持一致", (305, y + 735), 36, accent)
    elif layout == "raw-json":
        u.panel(d, (60, y + 30, 570, y + 700), (5, 9, 17))
        label(d, "RAW / 脱敏", (105, y + 75), 34, accent)
        for i, text in enumerate(["{", '  "model": unknown', '  "usage": unknown', '  "cost": unknown', "}"]):
            label(d, text, (105, y + 175 + i * 85), 29, fg, max_w=420)
        base.arrow(d, (600, y + 360), (690, y + 360), accent)
        u.panel(d, (720, y + 170, 1020, y + 550), (9, 14, 26))
        label(d, "汇总", (800, y + 240), 48, fg)
        label(d, "可追回", (790, y + 370), 36, accent)
        label(d, "不是只留截图", (360, y + 770), 36, accent)
    elif layout == "ab-lanes":
        node(d, (310, y), "同一输入 / 同一条件", accent, fg, 460, 130)
        for i, (name, run) in enumerate([("A", "run_A_demo"), ("B", "run_B_demo")]):
            yy = y + 250 + i * 270
            u.panel(d, (90, yy, 990, yy + 210), (9, 14, 26))
            label(d, name, (135, yy + 55), 68, accent)
            label(d, run, (285, yy + 45), 40, fg)
            label(d, "脱敏占位 · 原始响应摘要", (285, yy + 120), 28, (180, 190, 210))
        label(d, "两轮都要能追回原始记录", (225, y + 800), 36, accent)
    elif layout == "readback-loop":
        for i, text in enumerate(["发出请求", "拿到 Generation ID", "回读同一条 Generation"]):
            yy = y + i * 225
            node(d, (140, yy), text, accent, fg, 800, 160)
            if i < 2:
                d.polygon([(520, yy + 173), (560, yy + 173), (540, yy + 210)], fill=accent)
        label(d, "核对 model / 时间 / usage / cost", (140, y + 710), 36, accent)
    elif layout == "boundary-gate":
        u.panel(d, (120, y + 20, 960, y + 235), (65, 18, 28))
        label(d, "BLOCKED", (285, y + 75), 78, (255, 125, 135))
        for i, text in enumerate(["health 200", "价格表", "单张截图"]):
            node(d, (70 + i * 315, y + 390), text, accent, fg, 290, 155)
        label(d, "权限 / 价格来源 / 回读证据", (170, y + 660), 40, fg)
        label(d, "缺证据，不宣布已验证", (265, y + 750), 38, accent)
    elif layout == "quality-balance":
        d.line((540, y + 130, 540, y + 610), fill=fg, width=12)
        d.line((210, y + 240, 870, y + 240), fill=accent, width=12)
        d.polygon([(490, y + 650), (590, y + 650), (540, y + 570)], fill=fg)
        for x, lines in [(95, ["成本", "速度"]), (685, ["质量", "关键失败"])]:
            d.line((x + 145, y + 240, x + 55, y + 450), fill=fg, width=4)
            d.line((x + 145, y + 240, x + 235, y + 450), fill=fg, width=4)
            u.panel(d, (x, y + 440, x + 290, y + 660), (9, 14, 26))
            label(d, " / ".join(lines), (x + 35, y + 515), 36, accent, max_w=230)
        label(d, "优化也要过质量门", (305, y + 760), 40, fg)
    elif layout == "stamp":
        u.panel(d, (72, y + 45, 1008, y + 710), (40, 17, 24))
        label(d, "PROTOTYPE", (135, y + 115), 68, (255, 140, 150))
        label(d, "L1 / 课程示意", (135, y + 250), 54, fg)
        for i, text in enumerate(["Generation 回读", "usage", "成本 / 延迟"]):
            label(d, f"{text}：未证明", (135, y + 390 + i * 80), 34, (255, 170, 180))
        label(d, "不是当前实例实测", (300, y + 780), 38, accent)
    elif layout == "cta":
        u.panel(d, (72, y + 55, 1008, y + 720), tuple(int(c * .35) for c in accent))
        label(d, "下一集 / LF-08", (130, y + 115), 38, fg)
        label(d, "点赞  /  点踩", (200, y + 255), 64, accent)
        base.arrow(d, (540, y + 385), (540, y + 470), accent)
        label(d, "Score", (400, y + 500), 68, fg)
        label(d, "别被一条反馈带偏", (280, y + 650), 38, fg)
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
    video = ROOT / "langfuse/videos/LF-07-cost-latency-xiaoxiao-v3.mp4"
    base.run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
              "-i", str(concat), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
              "-b:a", "128k", "-movflags", "+faststart", str(video)])
    srt, vtt = [], ["WEBVTT", ""]
    for i, item in enumerate(timeline, start=1):
        srt += [str(i), f"{base.ts(item['start'], True)} --> {base.ts(item['end'], True)}", item["caption"], ""]
        vtt += [f"{base.ts(item['start'])} --> {base.ts(item['end'])}", item["caption"], ""]
    srt_path = ROOT / "langfuse/captions/LF-07-xiaoxiao-v3.srt"
    vtt_path = ROOT / "langfuse/captions/LF-07-xiaoxiao-v3.vtt"
    srt_path.write_text("\n".join(srt), encoding="utf-8")
    vtt_path.write_text("\n".join(vtt), encoding="utf-8")
    (BUILD / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"video": str(video), "duration": base.duration(video), "shots": len(timeline),
                      "last_caption_end": timeline[-1]["end"]}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
