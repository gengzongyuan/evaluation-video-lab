# LF-11 Xiaoxiao 原速版验收

日期：2026-11-23（Asia/Shanghai）

## 文件

- 视频：`langfuse/videos/LF-11-compare-xiaoxiao-v3.mp4`
- 字幕：`langfuse/captions/LF-11-xiaoxiao-v3.srt`、`langfuse/captions/LF-11-xiaoxiao-v3.vtt`
- 渲染器：`langfuse/scripts/render_lf11_xiaoxiao_v3.py`
- 分镜来源：`langfuse/LF-11-shot-board-xiaoxiao.md`
- 声线：`zh-CN-XiaoxiaoNeural`，`rate=-5%`
- 状态：`prototype / L1`

## 实测

- 成片 170.900 秒（2 分 51 秒）；20 段独立原速配音，无音频拉伸、无尾部静音填充。
- 20 段渲染口播与 LF-11 Xiaoxiao 分镜板逐字一致，没有改词。
- 视频 1080×1920，H.264；音频 AAC。
- 音视频时长差 0.016 秒，尾部静音 0.000 秒。
- `volumedetect`：mean -19.6 dB，max -1.6 dB。
- 20 个唯一镜头 ID、20 种构图；单镜约 7.320–10.032 秒。抽帧检查 0s、85s、155s，底部字幕清楚可见。
- 每镜底部烧录字幕；SRT/VTT 各 20 条，时间轴一致，最后一条均为 170.904 秒。
- 自然旁白质量门退出码 0，结果 `PASS`（含 full_decode）。
- Prompt/模型版本、run、分数、成本和延迟均为示意或留空。
- 视频、字幕、渲染器和本 QA 未发现 `U+FFFD`、内网地址或密钥字样。

质量门命令：

```bash
python3 langfuse/scripts/check_natural_voice_video.py \
  langfuse/videos/LF-11-compare-xiaoxiao-v3.mp4 \
  --subtitle langfuse/captions/LF-11-xiaoxiao-v3.srt \
  --subtitle langfuse/captions/LF-11-xiaoxiao-v3.vtt \
  --shots langfuse/build/lf11-xiaoxiao-v3/timeline.json
```

## 证据边界

本片只解释用同一 Dataset 比较 Prompt 或模型的概念口径。不证明当前实例已完成两个 run、Score 回读或任何候选全面领先。

## 主 agent 抽帧

按 20 个镜头中点抽帧：构图全部不同，底部烧录字幕可见。第 14 镜 10.032 秒略超 10 秒，保持原速。Prompt/模型版本、分数和成本均为示意。
