# LF-10 v2 媒体 QA

- 180 秒、12 个约 15 秒镜头、中文 TTS。
- 画面依次展示 Agent、retrieval、Tool、Generation、父子关系、状态和回读边界。
- 质量门：ffprobe、volumedetect、0/15/30/60/120/165 秒抽帧通过。
- SRT/VTT 非空，15 秒时间码；没有敏感凭据或内网地址。
- 证据边界：`prototype / L1`；示意调用树不代表当前实例真实 Trace。
