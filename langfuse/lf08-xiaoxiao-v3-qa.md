# LF-08 Xiaoxiao 原速版验收

日期：2026-11-23（Asia/Shanghai）

## 文件

- 视频：`langfuse/videos/LF-08-feedback-xiaoxiao-v3.mp4`
- 字幕：`langfuse/captions/LF-08-xiaoxiao-v3.srt`、`langfuse/captions/LF-08-xiaoxiao-v3.vtt`
- 渲染器：`langfuse/scripts/render_lf08_xiaoxiao_v3.py`
- 分镜来源：`langfuse/LF-08-shot-board-xiaoxiao.md`
- 声线：`zh-CN-XiaoxiaoNeural`，`rate=-5%`
- 状态：`prototype / L1`

## 实测

- 成片 173.166 秒（2 分 53 秒）；20 段独立原速配音，无音频拉伸、无尾部静音填充。
- 20 段渲染口播与 LF-08 Xiaoxiao 分镜板逐字一致，没有改词。
- 视频 1080×1920，H.264；音频 AAC。
- 音视频时长差 0.041 秒，尾部静音 0.000 秒。
- `volumedetect`：mean -19.6 dB，max -1.0 dB。
- 20 个唯一镜头 ID、20 种构图；单镜约 7.560–9.744 秒。抽帧检查 0s、85s、155s，底部字幕清楚可见。
- 每镜底部烧录字幕；SRT/VTT 各 20 条，时间轴一致，最后一条均为 173.232 秒。
- 自然旁白质量门退出码 0，结果 `PASS`（含 full_decode）。
- 点赞、点踩、评论、满意度和回归结果均为示意。
- 视频、字幕、渲染器和本 QA 未发现 `U+FFFD`、内网地址或密钥字样。

质量门命令：

```bash
python3 langfuse/scripts/check_natural_voice_video.py \
  langfuse/videos/LF-08-feedback-xiaoxiao-v3.mp4 \
  --subtitle langfuse/captions/LF-08-xiaoxiao-v3.srt \
  --subtitle langfuse/captions/LF-08-xiaoxiao-v3.vtt \
  --shots langfuse/build/lf08-xiaoxiao-v3/timeline.json
```

## 证据边界

本片只解释用户反馈如何关联 Trace、写成 Score、抽查正负空值并回流 Dataset 的概念口径。不证明当前实例已收到反馈、写入 Score、完成回读或修复问题。

## 主 agent 抽帧

按 20 个镜头中点抽帧：构图全部不同，底部烧录字幕可见。首/中/尾画面无乱码。第 13 镜口播稿有一处繁体「好評」，画面字幕为简体「好评」；不阻断媒体门，后续口播冻结时改回简体。
