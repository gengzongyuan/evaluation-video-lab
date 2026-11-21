# LF-03 v2 QA

- 12 个约 15 秒镜头，分别展示 Agent、Span、Generation、Tool、父子关系和回读字段。
- 中文旁白：macOS `say -v Eddy (中文（中国大陆）)`。
- `check_video_quality.py`：PASS；0/15/30/60/120/165 秒 6/6 抽帧哈希不同，音频非静音，180.046 秒，H.264/AAC，SRT/VTT 非空。
- 画面与旁白仍为课程示意，不证明当前 Langfuse 实例新 Trace 写入或回读。
