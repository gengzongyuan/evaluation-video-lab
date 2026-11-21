# LF-08 v2 播放器接入前置门

## 目标

LF-08 讲用户反馈如何回流到 Score。接入播放器前必须同时满足媒体门、字幕门和事实边界门；存在可播放 MP4 不等于已经证明反馈写入或用户满意度。

## 媒体门

- MP4 非空，时长约 180 秒（±1 秒）。
- 画面为 1080×1920，H.264；音频为 AAC 且 `volumedetect` 的 `mean_volume`、`max_volume` 不为 `-inf`。
- 在 0、15、30、60、120、165 秒抽帧成功，至少 3 个不同画面哈希；至少 12 个约 15 秒镜头。
- SRT/VTT 非空，UTF-8 可解码；每个镜头时间码与旁白段落一致，不得出现把 15 秒写成 15 分钟的格式。

## 内容与证据门

- 画面可以展示脱敏反馈、`trace_id`、反馈来源、正例/负例/空值、Score/事件和回流 Dataset 的示意结构。
- 旁白必须区分：反馈事件已记录、反馈已绑定到 Trace/Observation、Score 已写入并回读、以及用户总体满意度；这些不是同一个结论。
- 反馈原文、输入输出和截图必须移除 PII、密钥、Authorization、完整 prompt 与内网地址。
- 必须明确采样方式、反馈缺失、空值规则、时间戳、来源和隐私处理；不能用少量主动反馈推导总体满意度。
- 当前项目没有安全注入 key 时，真实反馈/Score 写入、Trace/Observation 关联、回读和 Dataset 回流均保持 `BLOCKED`，视频标记 `prototype / L1`。

## 验证命令

```bash
python3 langfuse/scripts/check_video_quality.py \
  langfuse/videos/LF-08-feedback-v2.mp4 \
  --subtitle langfuse/captions/LF-08-v2.srt \
  --subtitle langfuse/captions/LF-08-v2.vtt
python3 langfuse/validate_manifest.py
```

媒体质量门通过后，仍需人工听看、核对字幕同步、审阅隐私脱敏，并由事实审计确认官方字段和当前 SDK/API 语义；只有这些都满足才可在播放器和 `series-index.md` 登记 LF-08 v2。
