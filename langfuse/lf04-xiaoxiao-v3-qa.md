# LF-04 Xiaoxiao 原速版验收

日期：2026-11-23（Asia/Shanghai）

## 文件

- 视频：`langfuse/videos/LF-04-prompt-version-xiaoxiao-v3.mp4`
- 字幕：`langfuse/captions/LF-04-xiaoxiao-v3.srt`、`langfuse/captions/LF-04-xiaoxiao-v3.vtt`
- 渲染器：`langfuse/scripts/render_lf04_xiaoxiao_v3.py`
- 分镜来源：`langfuse/LF-04-shot-board-xiaoxiao.md`
- 声线：`zh-CN-XiaoxiaoNeural`，`rate=-5%`
- 状态：`prototype / L1`

## 实测

- 成片 166.866 秒（2 分 47 秒）；20 段独立原速配音，无音频拉伸、无尾部静音填充。
- 20 段渲染口播与 LF-04 Xiaoxiao 分镜板逐字一致，没有改词。
- 视频 1080×1920，H.264；音频 AAC。
- 音视频时长差 0.018 秒，尾部静音 0.000 秒。
- `volumedetect`：mean -19.7 dB，max -2.2 dB。
- 20 个唯一镜头 ID、20 种构图；单镜约 7.104–9.768 秒。抽帧检查 0s、80s、150s，底部字幕清楚可见。
- 每镜底部烧录字幕；SRT/VTT 各 20 条，时间轴一致，最后一条均为 166.920 秒。
- 自然旁白质量门退出码 0，结果 `PASS`。
- `python3 -m py_compile langfuse/scripts/render_lf04_xiaoxiao_v3.py` 通过。
- 视频、字幕、渲染器和本 QA 未发现 `U+FFFD`、内网地址或密钥字样。

质量门命令：

```bash
python3 langfuse/scripts/check_natural_voice_video.py \
  langfuse/videos/LF-04-prompt-version-xiaoxiao-v3.mp4 \
  --subtitle langfuse/captions/LF-04-xiaoxiao-v3.srt \
  --subtitle langfuse/captions/LF-04-xiaoxiao-v3.vtt \
  --shots langfuse/build/lf04-xiaoxiao-v3/timeline.json
```

## 证据边界

Prompt 名 `answer-guide-demo`、版本和 label 均为示意。本片只解释 Prompt 管理、版本、label 与回指口径；不证明当前实例已创建版本、修改 label 或完成 Trace 回读，也不把 production label 说成质量验收通过。
