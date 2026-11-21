# LF-04 v2 QA

- 12 个约 15 秒镜头，围绕 Prompt 版本、label、Trace metadata 和对比实验逐镜变化。
- 中文旁白：macOS `say -v 'Eddy (中文（中国大陆）)'`。
- 质量门：180.046 秒、1080x1920、H.264/AAC、音频非静音、6/6 抽帧时间点有变化、SRT/VTT 非空。
- 字幕人工检查：已修复“差��”乱码为“差异”；时间码按 15 秒分段。
- 证据边界：`prototype / L1`；没有真实 Prompt 创建、label 解析或 Trace 回读证明。
