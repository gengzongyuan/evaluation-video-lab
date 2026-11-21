# LF-09 v2 媒体 QA

- 180 秒，12 个约 15 秒镜头，中文 TTS。
- 画面覆盖 sampling、redaction、retention、权限、密钥轮换、告警和小流量发布。
- 不包含内网地址、项目 key、secret、Authorization 或 PII。
- 质量门需复核：ffprobe、volumedetect、0/15/30/60/120/165 秒抽帧、SRT/VTT。
- 证据边界：`prototype / L1`；不代表当前部署已通过安全或隐私验收。
