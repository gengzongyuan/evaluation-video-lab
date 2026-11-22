#!/usr/bin/env python3
"""Render LF-12 incident-to-fix with original-speed Xiaoxiao and burned captions."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "langfuse/build/lf12-xiaoxiao-v3"
BOARD = ROOT / "langfuse/LF-12-shot-board-xiaoxiao.md"
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
    ("01", "钩子", "异常信号不是根因结论", ["监控入口"]),
    ("02", "信号卡", "先固定时间窗、版本和指标口径", ["不填虚构数值"]),
    ("03", "选 Trace", "从异常分组进入原始 Trace", ["截图辅助"]),
    ("04", "瀑布", "先定位失败节点和偏离起点", ["失败高亮"]),
    ("05", "核对卡", "核对输入、输出、错误和状态", ["报错", "低质量"]),
    ("06", "根因网格", "根因分类，不等于自动找到根因", ["六类"]),
    ("07", "假设证据", "假设需要证据，也需要可反驳", ["反例入口"]),
    ("08", "commit 卡", "修复必须对应具体 commit 和版本", ["脱敏占位"]),
    ("09", "隔离闸门", "修复时只改一个变量，避免混杂", ["一扇门"]),
    ("10", "回归集", "失败样本进入固定回归集", ["item ID"]),
    ("11", "冻结配置", "回归要固定同一组题和评分规则", ["五项锁定"]),
    ("12", "重跑", "修复后用同一回归集重跑", ["新 run"]),
    ("13", "前后对照", "原失败样本要逐条前后对照", ["before / after"]),
    ("14", "新增失败", "还要看新增失败和关键场景回退", ["检查区"]),
    ("15", "回读闭环", "同一 run、item 回读修复结果", ["四步"]),
    ("16", "回滚门槛", "发布前定义告警、回滚和责任人", ["数值留空"]),
    ("17", "趋势边界", "一次回归成功 ≠ 长期稳定", ["仍需观察"]),
    ("18", "发布门", "三类证据齐全，才进入发布复核", ["缺一项关闭"]),
    ("19", "本集边界", "不是修复已验证", ["prototype / L1"]),
    ("20", "下一集", "自托管架构与健康检查", ["LF-13"]),
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
    draw.text((72, 62), f"LF-12  ·  {shot['kicker']}", font=u.font(28, True), fill=accent)
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
    danger = (255, 140, 150)
    muted = (180, 190, 210)
    if layout == "hook":
        u.panel(d, (80, y + 30, 1000, y + 390))
        d.line((140, y + 320, 930, y + 320), fill=(75, 86, 108), width=3)
        points = [(150, y + 285), (280, y + 265), (410, y + 280), (540, y + 245), (660, y + 250), (790, y + 80), (920, y + 65)]
        d.line(points, fill=danger, width=8, joint="curve")
        for px, py in points:
            d.ellipse((px-10, py-10, px+10, py+10), fill=danger)
        label(d, "异常信号 ↑", (140, y + 80), 40, fg)
        node(d, (250, y + 470), "模型根因？", accent, fg, 580, 180)
        label(d, "先调查，不先下结论", (300, y + 700), 34, muted)
    elif layout == "signal-card":
        for i, (name, value) in enumerate([("时间窗口", "待记录"), ("运行版本", "待锁定"), ("指标口径", "先写定义")]):
            yy = y + 30 + i * 215
            u.panel(d, (90, yy, 990, yy + 180))
            label(d, name, (140, yy + 35), 38, fg)
            label(d, value, (650, yy + 45), 32, accent)
        label(d, "三个条件缺一项，就先别比较", (180, y + 700), 34, muted)
    elif layout == "trace-pick":
        u.panel(d, (70, y + 70, 470, y + 440))
        label(d, "Dashboard", (120, y + 110), 36, accent)
        for i in range(3):
            u.rounded(d, (120, y + 200 + i*60, 410, y + 225 + i*60), 8, (60, 70, 90))
        d.ellipse((350, y + 300, 390, y + 340), fill=danger)
        d.line((440, y + 320, 610, y + 320), fill=accent, width=5)
        d.polygon([(610, y+320), (575, y+300), (575, y+340)], fill=accent)
        node(d, (610, y + 220), "原始 Trace", accent, fg, 380, 200)
        u.panel(d, (180, y + 520, 900, y + 700))
        label(d, "截图只作辅助证据", (260, y + 585), 36, fg)
    elif layout == "waterfall":
        u.panel(d, (60, y + 20, 440, y + 680))
        label(d, "调用树", (110, y + 60), 34, accent)
        for i, name in enumerate(["Trace", "Span", "Tool", "Generation"]):
            yy = y + 150 + i * 120
            node(d, (100 + i*25, yy), name, danger if i == 2 else accent, fg, 260, 90)
        u.panel(d, (480, y + 20, 1020, y + 680))
        label(d, "时间瀑布", (530, y + 60), 34, accent)
        for i, (name, width) in enumerate([("retrieve", 270), ("parse", 210), ("tool", 390), ("generate", 250)]):
            yy = y + 170 + i * 120
            label(d, name, (520, yy), 26, fg)
            u.rounded(d, (520, yy + 48, 520 + width, yy + 82), 8, danger if name == "tool" else accent)
        label(d, "失败节点高亮", (610, y + 640), 30, danger)
    elif layout == "inspect":
        fields = [("input", "已脱敏"), ("output", "待核对"), ("error", "分开记录"), ("status", "待核对"), ("latency", "不填虚构值")]
        for i, (name, state) in enumerate(fields):
            yy = y + 20 + i * 130
            u.panel(d, (90, yy, 990, yy + 105))
            label(d, name, (135, yy + 28), 32, accent)
            label(d, state, (630, yy + 32), 30, fg)
        label(d, "报错 ≠ 低质量，分开判断", (220, y + 710), 34, muted)
    elif layout == "root-cause-grid":
        causes = ["模型", "工具", "数据", "权限", "配置", "环境"]
        for i, name in enumerate(causes):
            xx = 80 + (i % 3) * 320
            yy = y + 50 + (i // 3) * 300
            node(d, (xx, yy), name, accent, fg, 280, 220)
            label(d, "待排查", (xx + 75, yy + 145), 28, muted)
        label(d, "分类不是自动诊断", (330, y + 690), 36, accent)
    elif layout == "hypothesis-evidence":
        u.panel(d, (70, y + 30, 520, y + 540))
        u.panel(d, (560, y + 30, 1010, y + 540))
        label(d, "根因假设", (130, y + 80), 40, accent)
        label(d, "支持证据", (620, y + 80), 40, accent)
        label(d, "最慢节点？", (130, y + 220), 36, fg)
        label(d, "日志 / 输入 / 输出", (620, y + 220), 30, fg)
        label(d, "还要找反例", (130, y + 390), 34, danger)
        label(d, "能反驳才可信", (620, y + 390), 34, fg)
        label(d, "慢，不一定就是根因", (290, y + 630), 38, muted)
    elif layout == "commit-card":
        u.panel(d, (90, y + 40, 990, y + 300))
        label(d, "commit", (140, y + 80), 34, accent)
        label(d, "脱敏占位 / 待填写", (140, y + 180), 42, fg)
        node(d, (90, y + 400), "变更摘要", accent, fg, 400, 180)
        node(d, (590, y + 400), "运行版本", accent, fg, 400, 180)
        d.line((540, y + 300, 290, y + 400), fill=accent, width=4)
        d.line((540, y + 300, 790, y + 400), fill=accent, width=4)
        label(d, "修复点必须能回指", (320, y + 660), 36, fg)
    elif layout == "isolation-gate":
        for i, (name, allowed) in enumerate([("Prompt", True), ("模型", False), ("数据", False), ("参数", False)]):
            yy = y + 30 + i * 155
            u.panel(d, (90, yy, 990, yy + 125))
            label(d, name, (140, yy + 35), 38, fg)
            label(d, "本次只改这一项" if allowed else "锁定", (570, yy + 42), 30, accent if allowed else muted)
        label(d, "变量混在一起，就无法归因", (210, y + 690), 34, danger)
    elif layout == "dataset-return":
        node(d, (250, y + 20), "原始失败样本", danger, fg, 580, 150)
        node(d, (90, y + 290), "脱敏", accent, fg, 400, 150)
        node(d, (590, y + 290), "审核", accent, fg, 400, 150)
        node(d, (250, y + 550), "固定回归 Dataset", accent, fg, 580, 150)
        d.line((540, y + 170, 290, y + 290), fill=accent, width=4)
        d.line((540, y + 170, 790, y + 290), fill=accent, width=4)
        d.line((290, y + 440, 450, y + 550), fill=accent, width=4)
        d.line((790, y + 440, 630, y + 550), fill=accent, width=4)
        label(d, "来源 + 稳定 item ID", (350, y + 740), 30, fg)
    elif layout == "freeze-regression":
        for i, name in enumerate(["Dataset", "模型", "Prompt", "参数", "评分规则"]):
            yy = y + 20 + i * 130
            u.panel(d, (90, yy, 990, yy + 105))
            label(d, name, (140, yy + 28), 34, fg)
            label(d, "LOCKED", (740, yy + 32), 28, accent, True)
        label(d, "同一组题，同一把尺", (320, y + 710), 36, fg)
    elif layout == "rerun-candidate":
        node(d, (90, y + 50), "固定回归集", accent, fg, 400, 170)
        node(d, (590, y + 50), "修复版本", accent, fg, 400, 170)
        d.line((290, y + 220, 460, y + 340), fill=accent, width=4)
        d.line((790, y + 220, 620, y + 340), fill=accent, width=4)
        node(d, (250, y + 340), "新 run / 待执行", accent, fg, 580, 170)
        for i, item in enumerate(["逐 item 输出", "运行时间", "run 标识"]):
            label(d, item, (150 + i*290, y + 610), 28, fg, max_w=250)
    elif layout == "before-after":
        for i, name in enumerate(["BEFORE / 修复前", "AFTER / 修复后"]):
            xx = 70 + i * 510
            u.panel(d, (xx, y + 30, xx + 430, y + 650))
            label(d, name, (xx + 35, y + 80), 30, accent, True, 360)
            for j in range(3):
                u.panel(d, (xx + 40, y + 190 + j*130, xx + 390, y + 290 + j*130))
                label(d, f"item_0{j+1}", (xx + 65, y + 215 + j*130), 28, fg)
                label(d, "待回读", (xx + 230, y + 220 + j*130), 26, muted)
        label(d, "逐条对照，不只看平均分", (260, y + 710), 34, fg)
    elif layout == "new-failure":
        node(d, (90, y + 70), "原失败样本", accent, fg, 400, 180)
        node(d, (590, y + 70), "结果待回读", accent, fg, 400, 180)
        u.panel(d, (90, y + 350, 990, y + 650), (65, 18, 28))
        label(d, "新增失败检查区", (150, y + 400), 42, danger)
        label(d, "关键场景回退？", (150, y + 530), 36, fg)
        label(d, "修好一条 ≠ 没碰坏别处", (250, y + 710), 34, muted)
    elif layout == "readback-loop":
        for i, item in enumerate(["修复 run", "同一 item", "Score / 输出 / 错误", "同轴回读"]):
            yy = y + i * 175
            node(d, (140, yy), item, accent, fg, 800, 140)
            if i < 3:
                d.polygon([(520, yy + 148), (560, yy + 148), (540, yy + 175)], fill=accent)
    elif layout == "rollback-threshold":
        u.panel(d, (90, y + 30, 990, y + 250))
        label(d, "告警 / 回滚门槛", (140, y + 80), 42, accent)
        label(d, "发布前定义，数值留空", (140, y + 165), 32, fg)
        node(d, (90, y + 350), "决策责任人", accent, fg, 400, 180)
        node(d, (590, y + 350), "退回上一版本", accent, fg, 400, 180)
        label(d, "关键回退时，知道谁来退、退到哪", (150, y + 640), 32, fg)
    elif layout == "trend-boundary":
        u.panel(d, (90, y + 40, 990, y + 650))
        d.line((160, y + 520, 900, y + 520), fill=(75, 86, 108), width=3)
        d.line((160, y + 150, 160, y + 520), fill=(75, 86, 108), width=3)
        d.ellipse((270, y + 330, 310, y + 370), fill=accent)
        label(d, "这一次成功", (330, y + 320), 36, accent)
        for i in range(4):
            d.ellipse((500+i*90, y + 265, 520+i*90, y + 285), outline=muted, width=3)
        label(d, "长期趋势仍需观察", (260, y + 590), 38, fg)
    elif layout == "release-gate":
        for i, item in enumerate(["异常 Trace", "修复 commit", "回归回读"]):
            node(d, (70 + i*330, y + 40), item, accent, fg, 290, 160)
            d.line((215 + i*330, y + 200, 540, y + 360), fill=accent, width=3)
        u.panel(d, (180, y + 360, 900, y + 630), (65, 18, 28))
        label(d, "发布复核门", (300, y + 420), 48, danger)
        label(d, "缺一项就保持关闭", (300, y + 540), 36, fg)
    elif layout == "stamp":
        u.panel(d, (72, y + 45, 1008, y + 710), (40, 17, 24))
        label(d, "PROTOTYPE", (135, y + 115), 68, danger)
        label(d, "L1 / 课程示意", (135, y + 250), 54, fg)
        for i, item in enumerate(["异常定位：未证明", "代码修复：未证明", "回归验证：未证明"]):
            label(d, item, (135, y + 390 + i*80), 34, (255, 170, 180))
    elif layout == "cta":
        u.panel(d, (72, y + 45, 1008, y + 720), tuple(int(c * .35) for c in accent))
        label(d, "下一集 / LF-13", (130, y + 95), 38, fg)
        label(d, "自托管架构与健康检查", (130, y + 210), 44, accent)
        for i, item in enumerate(["Web", "Worker", "DB", "Redis", "对象存储"]):
            xx = 105 + (i % 3)*300
            yy = y + 380 + (i//3)*170
            node(d, (xx, yy), item, accent, fg, 260, 120)
        label(d, "health / readiness 各能证明什么？", (160, y + 700), 30, fg)
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
    video = ROOT / "langfuse/videos/LF-12-debug-regression-xiaoxiao-v3.mp4"
    base.run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
              "-i", str(concat), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
              "-b:a", "128k", "-movflags", "+faststart", str(video)])
    srt, vtt = [], ["WEBVTT", ""]
    for i, item in enumerate(timeline, start=1):
        srt += [str(i), f"{base.ts(item['start'], True)} --> {base.ts(item['end'], True)}", item["caption"], ""]
        vtt += [f"{base.ts(item['start'])} --> {base.ts(item['end'])}", item["caption"], ""]
    (ROOT / "langfuse/captions/LF-12-xiaoxiao-v3.srt").write_text("\n".join(srt), encoding="utf-8")
    (ROOT / "langfuse/captions/LF-12-xiaoxiao-v3.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (BUILD / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"video": str(video), "duration": base.duration(video), "shots": len(timeline),
                      "last_caption_end": timeline[-1]["end"]}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
