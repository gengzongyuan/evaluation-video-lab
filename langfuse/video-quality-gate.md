# 短视频音画质量门

`check_video_quality.py` 用来拦截“文件存在但不能看”的原型视频。它不是内容验收，也不证明 Langfuse 运行证据；它只检查媒体可播放性和基本观看门槛。

## 检查项

- 时长约 180 秒（默认容差 ±1 秒）
- 1080×1920 竖屏
- H.264 视频流和 AAC 音频流
- 音频 `mean_volume`、`max_volume` 不能为 `-inf`
- 传入的 SRT/VTT 文件存在且非空
- 在 0、15、30、60、120、165 秒抽帧，至少有 3 个不同画面哈希，拦截固定单画面

## 用法

```bash
python3 langfuse/scripts/check_video_quality.py \
  langfuse/videos/LF-01-langfuse-overview-v2.mp4 \
  --subtitle langfuse/captions/LF-01-v2.srt \
  --subtitle langfuse/captions/LF-01-v2.vtt
```

通过只表示音画和文件门槛通过；仍需人工听看旁白、检查字幕同步、检查信息密度，并确认 `prototype / L1` 的证据边界没有被画面扩大。

## LF-01 v2 实测

- 时长：180.046 秒
- 画面：1080×1920，H.264
- 音频：AAC，`mean_volume=-26.0 dB`，`max_volume=-1.7 dB`
- 抽帧：0/15/30/60/120/165 秒，至少 3 个不同画面
- 字幕：SRT/VTT 均非空
- 结论：`PASS`（媒体门），内容和真实 Langfuse 运行证据仍需另外验收。
