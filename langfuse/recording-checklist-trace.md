# LF-02 Trace 真实实例录制清单

目标：在 Langfuse 4.79.0 本地实例上证明“一次脱敏请求能被记录并在 UI 中查询”，不证明模型质量或服务容量。

## 录制前

- [ ] 使用 `http://172.16.33.136:3000`，不要把内网地址发布到公开视频。
- [ ] 重新请求 `/api/public/health?failIfDatabaseUnavailable=true`，保存返回的 status/version。
- [ ] 锁定 SDK 名称与版本；密钥只放环境变量，不写脚本、终端录屏或仓库。
- [ ] 准备不含个人信息的输入，例如“把这句话改成三条要点”。

## 最小运行步骤

1. 安装官方 Python 或 JS/TS SDK，记录精确版本。
2. 设置 `LANGFUSE_PUBLIC_KEY`、`LANGFUSE_SECRET_KEY`、`LANGFUSE_BASE_URL`。
3. 按当前官方 SDK quickstart 创建一次 Trace 和一个模型调用 Observation。
4. 等待 SDK flush/shutdown；保存终端日志和运行时间。
5. 在 Web UI 按时间或 Trace 名称搜索，打开详情页。
6. 截取输入、输出、时间、Observation 类型和元数据字段；对 key、URL、业务文本做脱敏。

## 画面要展示

- 代码中的 Trace/Observation 父子关系。
- 终端中“发送成功/flush 完成”的日志（不可出现密钥）。
- UI 的 Trace 列表和详情页。
- 证据卡：版本、运行日期、输入类型、是否成功、未证明范围。

## 失败排查

- UI 无数据：先检查 Base URL、项目 key、网络和 flush；不要先改评分逻辑。
- health 正常但 SDK 失败：分别记录 Web 健康与客户端错误，不能把健康端点当成写入成功。
- 录制出现真实业务文本：立即删除素材并重新生成脱敏输入。

依据：本仓库 `LANGFUSE_DEPLOYED_INSTANCE_172.16.33.136.md`、`LANGFUSE_DEPLOYMENT_RUNBOOK.md` 的实例与验收记录；具体 SDK 参数以官方文档当前版本为准。

## v4 events_only 现场补充（2026-11-22）

当前 4.79.0 实例的旧 `/api/public/traces` 与 `/api/public/observations` 查询路径返回 404，响应建议使用升级后的 SDK/OTEL 协议。下一次受保护运行必须：

1. 使用当前官方 SDK/OTEL 接入方式发送 Trace（目标入口为 `/api/public/otel/v1/traces`，具体 headers/字段以当前官方文档为准）。
2. 保存 OTEL 发送响应、Trace ID、SDK 版本和运行 commit。
3. 使用当前 v4 支持的 UI/API 查询方法回读，不能继续把旧版 endpoint 当作验收命令。
4. 将旧路径 404 作为迁移边界写进视频，避免观众照抄过时命令。
