# LF-02 Xiaoxiao 原速版验收

日期：2026-11-23（Asia/Shanghai）

## 文件

- 视频：`langfuse/videos/LF-02-trace-xiaoxiao-v3.mp4`
- 字幕：`langfuse/captions/LF-02-xiaoxiao-v3.srt`、`langfuse/captions/LF-02-xiaoxiao-v3.vtt`
- 渲染器：`langfuse/scripts/render_lf02_xiaoxiao_v3.py`
- 声线：`zh-CN-XiaoxiaoNeural`，`rate=-5%`
- 状态：`prototype / L1`

## 实测

- 成片 161.003 秒（2 分 41 秒）；20 段独立原速配音，无音频拉伸、无尾部静音填充。
- 20 段渲染口播与 `LF-02-voice-script-xiaoxiao.md` 逐字一致，没有改词。
- 视频 1080×1920，H.264；音频 AAC。
- 音视频时长差 0.000 秒，尾部静音 0.000 秒。
- `volumedetect`：mean -19.7 dB，max -2.9 dB。
- 20 个唯一镜头 ID、20 种构图；单镜约 6.288–11.112 秒。实际抽帧检查首帧和 130 秒附近画面，底部字幕清楚可见。
- 每镜底部烧录字幕；SRT/VTT 各 20 条，时间轴一致，最后一条均为 00:02:34.656 → 00:02:41.016。
- 自然旁白质量门退出码 0，结果 `PASS`。
- `python3 -m py_compile langfuse/scripts/render_lf02_xiaoxiao_v3.py` 通过；`git diff --check` 通过。
- 视频、字幕和渲染器未发现 `U+FFFD`、内网地址或密钥字样。

质量门命令：

```bash
python3 langfuse/scripts/check_natural_voice_video.py \
  langfuse/videos/LF-02-trace-xiaoxiao-v3.mp4 \
  --subtitle langfuse/captions/LF-02-xiaoxiao-v3.srt \
  --subtitle langfuse/captions/LF-02-xiaoxiao-v3.vtt \
  --shots langfuse/build/lf02-xiaoxiao-v3/timeline.json
```

## 证据边界

`tr_demo_001` 在画面中明确标为示意 ID。本片只解释 Trace、Observation、Span、Generation 及验收口径；不证明当前实例已完成 Trace 写入、Worker 消费或 UI/API 回读，也不以单条 Trace 推断整体稳定性。
