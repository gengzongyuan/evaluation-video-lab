#!/usr/bin/env python3
"""Render LF-09 governance with original-speed Xiaoxiao and burned captions."""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "langfuse/build/lf09-xiaoxiao-v3"
BOARD = ROOT / "langfuse/LF-09-shot-board-xiaoxiao.md"
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
    ("01", "钩子", "记录更多，不等于观测更好", ["隐私", "费用", "噪声"]),
    ("02", "Sampling · 采样", "减少记录，也改变可见范围", ["采集范围"]),
    ("03", "采样边界", "采样结果不能当成全量结果", ["标明分母"]),
    ("04", "采样偏差", "采样规则会改变你看到的偏差", ["成功", "失败"]),
    ("05", "成本边界", "采样比例不能直接证明节省金额", ["金额留空"]),
    ("06", "Masking · 脱敏", "脱敏要覆盖输入、输出和发送前链路", ["离开应用前"]),
    ("07", "脱敏测试", "用虚构标记验证是否漏出", ["非真实 PII"]),
    ("08", "残留风险", "启用脱敏，不等于所有 PII 已删除", ["仍需审计"]),
    ("09", "Retention · 保留", "保留配置，不等于删除已执行", ["执行回读"]),
    ("10", "副本边界", "主库删除，不代表副本都删除", ["备份", "导出"]),
    ("11", "最小权限", "查看、修改、导出都要最小授权", ["角色矩阵"]),
    ("12", "密钥轮换", "密钥要轮换，但绝不展示真实值", ["仅占位符"]),
    ("13", "公开视频边界", "地址、登录信息和项目标识都要脱敏", ["公开可见"]),
    ("14", "告警噪声", "只有错误总量，告警很难行动", ["缺少上下文"]),
    ("15", "可行动告警", "告警要能回到 Trace 和失败样本", ["负责人", "升级"]),
    ("16", "证据闭环", "配置存在，不等于当前部署已生效", ["本轮回读"]),
    ("17", "小流量", "同时观察质量与数据风险", ["阈值待填"]),
    ("18", "回滚", "治理变更也要保留回滚路径", ["授权", "复核"]),
    ("19", "本集边界", "不是生产安全已验收", ["prototype / L1"]),
    ("20", "下一集", "拆开多步骤 Agent 调用树", ["LF-10"]),
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
    draw.text((72, 62), f"LF-09  ·  {shot['kicker']}", font=u.font(28, True), fill=accent)
    label(draw, shot["title"], (72, 118), 54, fg, max_w=930)
    draw.text((72, 252), f"{idx:02d} / 20    prototype / L1", font=u.font(24, True), fill=(185, 195, 215))
    u.rounded(draw, (72, 304, 1008, 314), 5, (41, 48, 65))
    u.rounded(draw, (72, 304, 72 + int(936 * idx / 20), 314), 5, accent)


def node(draw, xy, text, accent, fg, width=260, height=140):
    base.node(draw, xy, text, accent, fg, width, height)


def arrow(draw, start, end, accent):
    base.arrow(draw, start, end, accent)


def draw_shot(shot, idx):
    bg, accent, fg = PALETTES[(idx - 1) % len(PALETTES)]
    im = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(im)
    header(d, shot, idx, accent, fg)
    y = 380
    layout = shot["layout"]
    if layout == "hook":
        for r in range(3):
            for c in range(4):
                x, yy = 80 + c * 240, y + 20 + r * 130
                u.panel(d, (x, yy, x + 210, yy + 100))
                label(d, "Trace", (x + 55, yy + 30), 30, fg)
        for i, text in enumerate(["隐私", "费用", "噪声"]):
            x = 80 + i * 320
            u.panel(d, (x, y + 460, x + 280, y + 670), (65, 18, 28))
            label(d, "!", (x + 110, y + 485), 54, (255, 130, 140))
            label(d, text, (x + 90, y + 570), 38, fg)
    elif layout == "gauge":
        d.arc((170, y + 30, 910, y + 770), 200, 340, fill=accent, width=28)
        d.line((540, y + 400, 730, y + 190), fill=fg, width=12)
        d.ellipse((510, y + 370, 570, y + 430), fill=accent)
        label(d, "Sampling", (370, y + 450), 58, fg)
        label(d, "采集范围由规则决定", (300, y + 570), 36, accent)
        label(d, "示意，不填采样率", (370, y + 690), 30, (180, 190, 210))
    elif layout == "sample-grid":
        label(d, "原始事件", (90, y + 20), 34, fg)
        for r in range(4):
            for c in range(6):
                x, yy = 90 + c * 150, y + 100 + r * 130
                selected = (r * 6 + c) % 5 == 0
                d.rounded_rectangle((x, yy, x + 110, yy + 90), radius=16,
                                    fill=accent if selected else (30, 36, 50))
        label(d, "高亮 = 被采中；分母必须写清", (180, y + 670), 38, accent)
    elif layout == "bias-scale":
        d.line((540, y + 180, 540, y + 610), fill=fg, width=10)
        d.line((240, y + 270, 840, y + 160), fill=accent, width=12)
        d.polygon([(440, y + 680), (640, y + 680), (540, y + 580)], fill=fg)
        for x, yy, text in [(120, y + 310, "只采成功"), (660, y + 200, "只采失败")]:
            u.panel(d, (x, yy, x + 300, yy + 170))
            label(d, text, (x + 55, yy + 55), 38, fg)
        label(d, "两边都不是全量", (360, y + 740), 36, accent)
    elif layout == "cost-warning":
        for i, text in enumerate(["采样", "usage", "价格", "实际流量"]):
            x = 80 + (i % 2) * 480
            yy = y + (i // 2) * 230
            node(d, (x, yy), text, accent, fg, 440, 160)
        u.panel(d, (180, y + 520, 900, y + 740), (65, 18, 28))
        label(d, "真实节省金额", (260, y + 560), 44, fg)
        label(d, "待实测，不能由示意比例直算", (240, y + 650), 32, (255, 150, 160))
    elif layout == "redaction-flow":
        for i, text in enumerate(["input", "output"]):
            node(d, (90, y + i * 230), text, accent, fg, 260, 150)
        node(d, (420, y + 100), "发送前脱敏", accent, fg, 300, 220)
        node(d, (790, y + 100), "观测链路", accent, fg, 220, 220)
        arrow(d, (350, y + 175), (420, y + 175), accent)
        arrow(d, (720, y + 210), (790, y + 210), accent)
        label(d, "不是只在展示页遮住", (300, y + 570), 44, accent)
    elif layout == "test-card":
        node(d, (300, y), "虚构敏感标记", accent, fg, 480, 140)
        for i, text in enumerate(["原始记录", "日志", "错误", "导出"]):
            x = 80 + (i % 2) * 480
            yy = y + 260 + (i // 2) * 220
            u.panel(d, (x, yy, x + 440, yy + 170))
            label(d, text, (x + 40, yy + 35), 38, fg)
            label(d, "检查是否漏出", (x + 40, yy + 105), 28, accent)
    elif layout == "false-shield":
        d.polygon([(540, y + 20), (820, y + 130), (770, y + 490), (540, y + 680),
                   (310, y + 490), (260, y + 130)], fill=(24, 48, 62), outline=accent)
        d.line((540, y + 40, 590, y + 260), fill=bg, width=30)
        d.line((590, y + 260, 525, y + 390), fill=bg, width=30)
        label(d, "规则覆盖", (390, y + 220), 44, fg)
        label(d, "仍有缺口", (410, y + 390), 44, (255, 140, 150))
        label(d, "残留风险需要单独审计", (290, y + 740), 38, accent)
    elif layout == "retention-timeline":
        d.line((150, y + 360, 930, y + 360), fill=accent, width=8)
        for i, (x, title, sub) in enumerate([(150, "创建", "时间戳"), (540, "到期", "策略期限"), (930, "删除", "待执行回读")]):
            d.ellipse((x - 28, y + 332, x + 28, y + 388), fill=fg)
            label(d, title, (x - 55, y + 220), 40, fg)
            label(d, sub, (x - 95, y + 430), 28, accent, max_w=220)
        label(d, "写了天数 ≠ 删除已发生", (280, y + 650), 44, fg)
    elif layout == "backup-split":
        node(d, (340, y), "主库删除", accent, fg, 400, 140)
        for i, text in enumerate(["备份", "导出", "其他副本"]):
            x = 60 + i * 340
            node(d, (x, y + 380), text, accent, fg, 300, 160)
            d.line((540, y + 140, x + 150, y + 380), fill=accent, width=4)
            label(d, "状态待核对", (x + 55, y + 580), 28, (255, 160, 170))
    elif layout == "permission-matrix":
        heads = ["角色", "查看", "修改", "导出"]
        for c, h in enumerate(heads):
            label(d, h, (90 + c * 235, y + 20), 30, accent, True, 200)
        for r, role in enumerate(["角色 A", "角色 B", "角色 C"]):
            for c in range(4):
                x, yy = 70 + c * 235, y + 100 + r * 180
                u.panel(d, (x, yy, x + 215, yy + 140))
                text = role if c == 0 else ("按授权" if (r + c) % 2 else "—")
                label(d, text, (x + 35, yy + 48), 30, fg, True, 160)
        label(d, "空格不是默认允许", (340, y + 690), 38, accent)
    elif layout == "key-rotation":
        for i, (title, sub) in enumerate([("旧 key", "••••••"), ("轮换记录", "时间 / 范围"), ("新 key", "••••••")]):
            x = 60 + i * 340
            u.panel(d, (x, y + 140, x + 300, y + 380))
            label(d, title, (x + 70, y + 175), 36, fg)
            label(d, sub, (x + 70, y + 255), 32, accent)
            if i < 2:
                arrow(d, (x + 300, y + 270), (x + 340, y + 270), accent)
        label(d, "时间 + 影响范围", (350, y + 500), 42, fg)
        label(d, "画面永远只显示占位符", (280, y + 620), 36, accent)
    elif layout == "secure-boundary":
        u.panel(d, (90, y + 20, 990, y + 700), (225, 232, 242))
        d.rounded_rectangle((90, y + 20, 990, y + 130), radius=24, fill=(45, 55, 72))
        label(d, "https://••••••••", (150, y + 55), 32, (230, 235, 245))
        for i, text in enumerate(["登录信息", "项目标识", "TLS / 权限验收"]):
            yy = y + 200 + i * 150
            label(d, text, (150, yy), 34, (30, 45, 65))
            d.rounded_rectangle((560, yy - 10, 900, yy + 60), radius=12, fill=(35, 42, 55))
            label(d, "已遮盖" if i < 2 else "待验证", (650, yy + 5), 28, (230, 235, 245))
    elif layout == "alert-card":
        u.panel(d, (120, y + 50, 960, y + 420), (65, 18, 28))
        label(d, "错误变多", (200, y + 110), 62, (255, 140, 150))
        label(d, "总量：示意", (200, y + 250), 42, fg)
        for i, text in enumerate(["版本？", "时间窗口？", "失败样本？"]):
            node(d, (100 + i * 320, y + 520), text, accent, fg, 280, 150)
    elif layout == "alert-tree":
        items = ["告警", "Trace", "版本", "失败样本", "负责人 / 升级"]
        for i, text in enumerate(items):
            yy = y + i * 145
            node(d, (150, yy), text, accent, fg, 780, 110)
            if i < len(items) - 1:
                d.polygon([(520, yy + 112), (560, yy + 112), (540, yy + 140)], fill=accent)
    elif layout == "evidence-check":
        for i, (text, state) in enumerate([("官方文档", "能力方向"), ("页面截图", "入口存在"), ("本轮配置", "待核对"), ("结果回读", "才能闭环")]):
            x = 80 + (i % 2) * 480
            yy = y + 30 + (i // 2) * 300
            u.panel(d, (x, yy, x + 440, yy + 240))
            label(d, text, (x + 45, yy + 45), 40, fg)
            label(d, state, (x + 45, yy + 140), 32, accent)
        label(d, "四张卡不能互相替代", (320, y + 690), 38, fg)
    elif layout == "canary":
        node(d, (80, y + 40), "小流量", accent, fg, 360, 150)
        node(d, (620, y + 40), "全量（未到）", (100, 110, 135), fg, 360, 150)
        for i, text in enumerate(["错误", "延迟", "成本", "敏感数据"]):
            x = 70 + (i % 2) * 490
            yy = y + 320 + (i // 2) * 200
            u.panel(d, (x, yy, x + 450, yy + 150))
            label(d, text, (x + 35, yy + 30), 36, fg)
            label(d, "阈值待业务基线", (x + 35, yy + 95), 26, accent)
    elif layout == "rollback-map":
        for i, text in enumerate(["变更版本", "小流量", "复核", "授权回滚"]):
            x = 55 + i * 255
            node(d, (x, y + 150), text, accent, fg, 230, 160)
            if i < 3:
                arrow(d, (x + 230, y + 230), (x + 255, y + 230), accent)
        d.arc((170, y + 360, 910, y + 720), 0, 180, fill=accent, width=6)
        label(d, "影响范围 + 负责人 + 复核结果", (210, y + 650), 38, fg)
    elif layout == "stamp":
        u.panel(d, (72, y + 45, 1008, y + 710), (40, 17, 24))
        label(d, "PROTOTYPE", (135, y + 115), 68, (255, 140, 150))
        label(d, "L1 / 课程示意", (135, y + 250), 54, fg)
        for i, text in enumerate(["采样回读：未证明", "脱敏 / 保留：未证明", "权限 / 告警：未证明"]):
            label(d, text, (135, y + 390 + i * 80), 34, (255, 170, 180))
    elif layout == "cta":
        u.panel(d, (72, y + 55, 1008, y + 720), tuple(int(c * .35) for c in accent))
        label(d, "下一集 / LF-10", (130, y + 115), 38, fg)
        label(d, "Agent 调用树", (130, y + 270), 58, accent)
        for i, text in enumerate(["调度", "Tool", "Generation"]):
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
    video = ROOT / "langfuse/videos/LF-09-governance-xiaoxiao-v3.mp4"
    base.run([FFMPEG, "-y", "-hide_banner", "-loglevel", "error", "-f", "concat", "-safe", "0",
              "-i", str(concat), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac",
              "-b:a", "128k", "-movflags", "+faststart", str(video)])
    srt, vtt = [], ["WEBVTT", ""]
    for i, item in enumerate(timeline, start=1):
        srt += [str(i), f"{base.ts(item['start'], True)} --> {base.ts(item['end'], True)}", item["caption"], ""]
        vtt += [f"{base.ts(item['start'])} --> {base.ts(item['end'])}", item["caption"], ""]
    (ROOT / "langfuse/captions/LF-09-xiaoxiao-v3.srt").write_text("\n".join(srt), encoding="utf-8")
    (ROOT / "langfuse/captions/LF-09-xiaoxiao-v3.vtt").write_text("\n".join(vtt), encoding="utf-8")
    (BUILD / "timeline.json").write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"video": str(video), "duration": base.duration(video), "shots": len(timeline),
                      "last_caption_end": timeline[-1]["end"]}, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
