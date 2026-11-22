# LF-07 Xiaoxiao 原速版验收

日期：2026-11-23（Asia/Shanghai）

## 文件

- 视频：`langfuse/videos/LF-07-cost-latency-xiaoxiao-v3.mp4`
- 字幕：`langfuse/captions/LF-07-xiaoxiao-v3.srt`、`langfuse/captions/LF-07-xiaoxiao-v3.vtt`
- 渲染器：`langfuse/scripts/render_lf07_xiaoxiao_v3.py`
- 分镜来源：`langfuse/LF-07-shot-board-xiaoxiao.md`
- 声线：`zh-CN-XiaoxiaoNeural`，`rate=-5%`
- 状态：`prototype / L1`

## 实测

- 成片 176.233 秒（2 分 56 秒）；20 段独立原速配音，无音频拉伸、无尾部静音填充。
- 20 段渲染口播与 LF-07 Xiaoxiao 分镜板逐字一致，没有改词。
- 视频 1080×1920，H.264；音频 AAC。
- 音视频时长差 0.025 秒，尾部静音 0.000 秒。
- `volumedetect`：mean -19.5 dB，max -0.8 dB。
- 20 个唯一镜头 ID、20 种构图；单镜约 7.848–10.512 秒。抽帧检查 0s、88s、160s，底部字幕清楚可见。
- 每镜底部烧录字幕；SRT/VTT 各 20 条，时间轴一致，最后一条均为 176.304 秒。
- 自然旁白质量门退出码 0，结果 `PASS`。
- `python3 -m py_compile langfuse/scripts/render_lf07_xiaoxiao_v3.py` 通过。
- 视频、字幕、渲染器和本 QA 未发现 `U+FFFD`、内网地址或密钥字样。

质量门命令：

```bash
python3 langfuse/scripts/check_natural_voice_video.py \
  langfuse/videos/LF-07-cost-latency-xiaoxiao-v3.mp4 \
  --subtitle langfuse/captions/LF-07-xiaoxiao-v3.srt \
  --subtitle langfuse/captions/LF-07-xiaoxiao-v3.vtt \
  --shots langfuse/build/lf07-xiaoxiao-v3/timeline.json
```

## 证据边界

token、金额、耗时、趋势、模型名和 run ID 均为示意或 `unknown`。本片只解释 Generation、usage、cost、latency 的看法和验收口径；不证明当前实例已完成 Generation 回读、真实用量、费用或延迟验证，也不以单条 Trace 推断 P95、SLA 或质量。
