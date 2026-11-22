#!/usr/bin/env python3
"""Render LF-04 with original-speed Xiaoxiao TTS and 20 captioned shots."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "langfuse" / "build" / "lf04-xiaoxiao-v3"
BOARD = ROOT / "langfuse" / "LF-04-shot-board-xiaoxiao.md"
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
    ("01", "钩子", "这次到底用了哪一版？", ["改一行", "先问版本"]),
    ("02", "散落", "散落各处，很难回溯", ["代码", "配置", "脚本"]),
    ("03", "Prompt 卡", "先给它名字和内容", ["示意名"]),
    ("04", "版本栈", "同一个名字，也要看版本", ["v1", "v2"]),
    ("05", "label 路标", "label 指向版本", ["test", "production"]),
    ("06", "运行时", "获取 → 填变量 → 交给模型", ["环境变量占位"]),
    ("07", "回指", "运行要能指回 Prompt 版本", ["待回读"]),
    ("08", "文本差异", "先看改了哪里", ["质量栏空白"]),
    ("09", "发布边界", "label 生效 ≠ 质量已验收", ["警告"]),
    ("10", "录制锁定", "先锁定版本、时间和返回值", ["占位符"]),
    ("11", "固定输入", "比较前先固定同一条输入", ["同一样本"]),
    ("12", "控制变量", "只改 Prompt 版本", ["模型锁定", "参数锁定"]),
    ("13", "分数边界", "分数要连同样本看", ["评分规则"]),
    ("14", "回滚线索", "知道退到哪一版", ["待确认"]),
    ("15", "发布核对", "缺一项先别宣称已发布", ["五项核对"]),
    ("16", "健康检查", "health 200 ≠ Prompt 已发布", ["未证明"]),
    ("17", "证据闭环", "同一个 Trace ID 回读版本", ["四步"]),
    ("18", "失败门", "认证或字段失败就停止", ["BLOCKED"]),
    ("19", "本集边界", "示意不是当前实例已发布", ["prototype / L1"]),
    ("20", "下一集", "用同一组样本做重复实验", ["LF-05"]),
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
    draw.text((72, 62), f"LF-04  ·  {shot['kicker']}", font=u.font(28, True), fill=accent)
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
        u.panel(d, (90, y + 40, 990, y + 280))
        label(d, "Prompt 只改了一行", (150, y + 120), 44, fg)
        label(d, "？", (430, y + 340), 180, accent)
        label(d, "输出区出现变化标记", (240, y + 620), 38, fg)
    elif layout == "scattered":
        for i, text in enumerate(["代码", "配置", "临时脚本"]):
            node(d, (90 + (i % 2) * 470, y + 40 + (i // 2) * 250), text, accent, fg, 400, 160)
        label(d, "连不上同一版本", (300, y + 620), 42, (255, 130, 140))
    elif layout == "prompt-card":
        u.panel(d, (90, y + 40, 990, y + 680), (240, 244, 248))
        label(d, "PROMPT", (150, y + 90), 32, (25, 50, 75))
        label(d, "answer-guide-demo", (150, y + 170), 48, (30, 45, 65))
        label(d, "{{question}}", (150, y + 320), 40, (35, 120, 105))
        label(d, "{{context}}", (150, y + 420), 40, (35, 120, 105))
        label(d, "示意名 · 脱敏变量", (150, y + 540), 32, (90, 100, 120))
    elif layout == "version-stack":
        for i, ver in enumerate(["v1", "v2"]):
            u.panel(d, (180, y + 80 + i * 260, 900, y + 280 + i * 260))
            label(d, ver, (230, y + 145 + i * 260), 64, accent)
            label(d, "概念示意 · 无效果分数", (430, y + 165 + i * 260), 28, fg)
        label(d, "排错看具体版本", (320, y + 680), 40, fg)
    elif layout == "label-road":
        node(d, (360, y), "Prompt 名", accent, fg, 360, 130)
        node(d, (90, y + 320), "test -> v1", accent, fg, 380, 150)
        node(d, (610, y + 320), "production -> v2", accent, fg, 380, 150)
        d.line((540, y + 130, 280, y + 320), fill=accent, width=4)
        d.line((540, y + 130, 800, y + 320), fill=accent, width=4)
        label(d, "没有升降箭头", (360, y + 560), 38, fg)
        label(d, "label 不是效果分数", (300, y + 650), 38, accent)
    elif layout == "code-fetch":
        for i, text in enumerate(["get_prompt()", "fill variables", "generate()"]):
            node(d, (140, y + i * 210), text, accent, fg, 800, 150)
            if i < 2:
                d.polygon([(520, y + 163 + i * 210), (560, y + 163 + i * 210), (540, y + 198 + i * 210)], fill=accent)
        label(d, "密钥只显示环境变量占位", (220, y + 680), 32, accent)
    elif layout == "trace-link":
        node(d, (90, y + 80), "Trace", accent, fg, 380, 180)
        node(d, (610, y + 80), "Prompt v?", accent, fg, 380, 180)
        d.line((470, y + 170, 610, y + 170), fill=(150, 160, 180), width=4)
        label(d, "虚线连接 · 待真实回读核对", (200, y + 380), 38, fg)
        label(d, "取到不等于已经回指成功", (230, y + 520), 40, accent)
    elif layout == "version-diff":
        u.panel(d, (60, y + 40, 500, y + 620))
        u.panel(d, (580, y + 40, 1020, y + 620))
        label(d, "v1", (220, y + 90), 40, accent)
        label(d, "请简洁回答", (120, y + 250), 36, fg)
        label(d, "v2", (740, y + 90), 40, accent)
        label(d, "请先给结论", (640, y + 250), 36, (255, 160, 120))
        label(d, "质量栏：空白", (370, y + 700), 38, (255, 140, 150))
    elif layout == "label-warning":
        u.panel(d, (90, y + 60, 990, y + 360))
        label(d, "production", (150, y + 140), 54, fg)
        label(d, "指向某个版本", (150, y + 230), 40, accent)
        u.panel(d, (90, y + 430, 990, y + 680), (50, 28, 18))
        label(d, "警告：发布闸门仍未打开", (150, y + 520), 40, (255, 180, 120))
    elif layout == "run-boundary":
        for i, text in enumerate(["Langfuse 版本", "SDK 版本", "运行时间", "实际 label"]):
            u.panel(d, (90, y + i * 160, 990, y + 130 + i * 160))
            label(d, text, (140, y + 35 + i * 160), 38, fg)
            label(d, "占位 / 待替换", (680, y + 40 + i * 160), 28, accent, True)
    elif layout == "fixed-input":
        node(d, (240, y), "同一输入 / 同一样本 ID", accent, fg, 600, 140)
        node(d, (90, y + 320), "Prompt A", accent, fg, 380, 180)
        node(d, (610, y + 320), "Prompt B", accent, fg, 380, 180)
        d.line((540, y + 140, 280, y + 320), fill=accent, width=4)
        d.line((540, y + 140, 800, y + 320), fill=accent, width=4)
        label(d, "不要一版简单题、一版难题", (220, y + 580), 36, accent)
    elif layout == "control-grid":
        for i, (name, state) in enumerate([("模型", "锁定"), ("参数", "锁定"), ("数据", "锁定"), ("Prompt 版本", "可切换")]):
            xx, yy = 70 + (i % 2) * 480, y + 20 + (i // 2) * 340
            u.panel(d, (xx, yy, xx + 440, yy + 290))
            label(d, name, (xx + 40, yy + 70), 44, fg)
            label(d, state, (xx + 40, yy + 160), 36, accent if state == "可切换" else (180, 190, 210))
    elif layout == "score-split":
        u.panel(d, (60, y + 40, 500, y + 650))
        label(d, "版本号", (160, y + 120), 44, accent)
        label(d, "分数：不填", (140, y + 280), 36, (255, 140, 150))
        u.panel(d, (580, y + 40, 1020, y + 650))
        label(d, "同一批样本", (640, y + 120), 36, fg)
        label(d, "同一评分规则", (640, y + 250), 36, fg)
        label(d, "失败案例", (640, y + 380), 36, fg)
    elif layout == "rollback":
        node(d, (200, y + 40), "当前版本", accent, fg, 680, 160)
        d.polygon([(540, y + 250), (500, y + 210), (580, y + 210)], fill=accent)
        node(d, (200, y + 280), "上一版", accent, fg, 680, 160)
        u.panel(d, (200, y + 520, 880, y + 680))
        label(d, "审批节点：待确认", (280, y + 565), 38, (255, 170, 120))
    elif layout == "checklist":
        items = ["Prompt 名", "版本", "label", "创建时间", "内容摘要"]
        for i, text in enumerate(items):
            yy = y + i * 130
            d.rounded_rectangle((90, yy, 160, yy + 70), radius=10, outline=accent, width=3)
            label(d, text, (200, yy + 15), 38, fg)
            label(d, "待核对", (780, yy + 20), 28, (180, 190, 210), True)
    elif layout == "not-equal":
        u.panel(d, (60, y + 120, 440, y + 520))
        u.panel(d, (640, y + 120, 1020, y + 520))
        label(d, "health", (140, y + 220), 44, fg)
        label(d, "200", (160, y + 320), 64, accent)
        label(d, "Prompt", (730, y + 220), 44, fg)
        label(d, "已验证?", (710, y + 320), 44, (255, 140, 150))
        label(d, "≠", (495, y + 270), 78, (255, 112, 120))
        label(d, "页面打开也不算发布成功", (230, y + 620), 36, accent)
    elif layout == "loop":
        for i, text in enumerate(["取回 Prompt", "跑一次请求", "拿到 Trace ID", "回读同一条"]):
            yy = y + i * 175
            node(d, (140, yy), text, accent, fg, 800, 140)
            if i < 3:
                d.polygon([(520, yy + 148), (560, yy + 148), (540, yy + 175)], fill=accent)
    elif layout == "evidence-gate":
        u.panel(d, (120, y + 20, 960, y + 220), (65, 18, 28))
        label(d, "STOP / BLOCKED", (250, y + 80), 58, (255, 125, 135))
        for i, text in enumerate(["401", "404", "字段对不上"]):
            node(d, (70 + i * 315, y + 320), text, accent, fg, 290, 150)
        label(d, "保留原始响应，不要用截图补结论", (140, y + 560), 34, fg)
    elif layout == "stamp":
        u.panel(d, (72, y + 45, 1008, y + 710), (40, 17, 24))
        label(d, "PROTOTYPE", (135, y + 115), 68, (255, 140, 150))
        label(d, "L1 / 课程示意", (135, y + 250), 54, fg)
        for i, text in enumerate(["创建版本：未证明", "修改 label：未证明", "Trace 回读：未证明"]):
            label(d, text, (135, y + 390 + i * 80), 34, (255, 170, 180))
    elif layout == "cta":
        u.panel(d, (72, y + 55, 1008, y + 720), tuple(int(c * .35) for c in accent))
        label(d, "下一集 / LF-05", (130, y + 115), 38, fg)
        label(d, "Dataset", (180, y + 280), 64, accent)
        label(d, "同一组样本", (180, y + 410), 48, fg)
        label(d, "比随手换几个问题更适合重复实验", (180, y + 560), 34, fg, max_w=760)
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
    video = ROOT / "langfuse/videos/LF-04-prompt-version-xiaoxiao-v3.mp4"
    base.run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
              "-i", str(concat), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
              "-b:a", "128k", "-movflags", "+faststart", str(video)])
    srt, vtt = [], ["WEBVTT", ""]
    for i, item in enumerate(timeline, start=1):
        srt += [str(i), f"{base.ts(item['start'], True)} --> {base.ts(item['end'], True)}", item["caption"], ""]
        vtt += [f"{base.ts(item['start'])} --> {base.ts(item['end'])}", item["caption"], ""]
    (ROOT / "langfuse/captions/LF-04-xiaoxiao-v3.srt").write_text("\n".join(srt), encoding="utf-8")
    (ROOT / "langfuse/captions/LF-04-xiaoxiao-v3.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (BUILD / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"video": str(video), "duration": base.duration(video), "shots": len(timeline),
                      "last_caption_end": timeline[-1]["end"]}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
