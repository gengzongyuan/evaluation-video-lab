# LF-02 v2 QA

- 12 个约 15 秒镜头，画面随 Trace 结构逐镜变化。
- 中文旁白：macOS `say -v Eddy (中文（中国大陆）)`。
- 已抽帧：0、15、30、60、120、165 秒。
- 已检查：ffprobe 时长/分辨率/音视频流，volumedetect 非静音。
- 状态：prototype / L1；不证明当前 Langfuse 实例新 Trace 写入或回读。
