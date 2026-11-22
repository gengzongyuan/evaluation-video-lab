# LF-09 Xiaoxiao 原速版验收

日期：2026-11-23（Asia/Shanghai）

## 文件

- 视频：`langfuse/videos/LF-09-governance-xiaoxiao-v3.mp4`
- 字幕：`langfuse/captions/LF-09-xiaoxiao-v3.srt`、`langfuse/captions/LF-09-xiaoxiao-v3.vtt`
- 渲染器：`langfuse/scripts/render_lf09_xiaoxiao_v3.py`
- 分镜来源：`langfuse/LF-09-shot-board-xiaoxiao.md`
- 声线：`zh-CN-XiaoxiaoNeural`，`rate=-5%`
- 状态：`prototype / L1`

## 实测

- 成片 182.876 秒（3 分 03 秒）；20 段独立原速配音，无音频拉伸、无尾部静音填充。
- 20 段渲染口播与 LF-09 Xiaoxiao 分镜板逐字一致，没有改词。
- 视频 1080×1920，H.264；音频 AAC。
- 音视频时长差 0.000 秒，尾部静音 0.000 秒。
- `volumedetect`：mean -19.7 dB，max -2.6 dB。
- 20 个唯一镜头 ID、20 种构图；单镜约 8.064–10.488 秒。抽帧检查 0s、90s、170s，底部字幕清楚可见。
- 每镜底部烧录字幕；SRT/VTT 各 20 条，时间轴一致，最后一条均为 182.904 秒。
- 自然旁白质量门退出码 0，结果 `PASS`（含 full_decode）。
- 采样率、金额、密钥和删除状态均为示意或占位，不展示真实值。
- 视频、字幕、渲染器和本 QA 未发现 `U+FFFD`、内网地址或密钥字样。

质量门命令：

```bash
python3 langfuse/scripts/check_natural_voice_video.py \
  langfuse/videos/LF-09-governance-xiaoxiao-v3.mp4 \
  --subtitle langfuse/captions/LF-09-xiaoxiao-v3.srt \
  --subtitle langfuse/captions/LF-09-xiaoxiao-v3.vtt \
  --shots langfuse/build/lf09-xiaoxiao-v3/timeline.json
```

## 证据边界

本片只解释采样、脱敏、保留、权限、告警和小流量治理的概念口径。不证明当前部署已生效采样回读、脱敏/保留删除、权限最小化或告警闭环。
