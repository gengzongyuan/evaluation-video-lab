# LF-01 v2 样片 QA

- 时长：`180.046029` 秒（约 180 秒）
- 画面：1080x1920，H.264
- 音频：AAC；`volumedetect`：mean `-26.0 dB`，max `-1.7 dB`，不是静音
- 镜头结构：12 个 15 秒镜头；时间点 0、15、30、60、120、165 秒均已抽帧
- 画面变化：每 15 秒切换标题、结构图或代码示意；不是固定单画面
- 旁白：macOS `say -v 'Eddy (中文（中国大陆）)'` 生成，逐镜头对应旁白文本
- 字幕：`captions/LF-01-v2.srt`、`captions/LF-01-v2.vtt`
- 证据边界：仍为 `prototype / L1`；没有真实 Langfuse Trace 写入或回读证明
