# LF-06 v2 媒体 QA

- 视频：`videos/LF-06-score-v2.mp4`
- 时长：180.046 秒
- 画面：1080×1920，H.264
- 音频：AAC，`volumedetect` 非静音
- 镜头：12 个约 15 秒镜头；0/15/30/60/120/165 秒抽帧均有变化
- 字幕：`captions/LF-06-v2.srt`、`captions/LF-06-v2.vtt`，非空且时间码为 15 秒分段
- 质量门：`python3 langfuse/scripts/check_video_quality.py ...` 输出 PASS
- 证据边界：`prototype / L1`；真实 Score 写入、回读和 Dataset run 仍为 `BLOCKED`
