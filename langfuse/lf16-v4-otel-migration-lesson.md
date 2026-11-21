# LF-16｜Langfuse v4：旧 API 为什么失效？

## 一句话结果
看完后，观众能识别 v4 `events_only` 的旧 API 迁移信号，并知道应升级当前 SDK/使用 OpenTelemetry，而不是继续重试旧 endpoint。

## 3 分钟结构

- 0–25s：请求旧 `/api/public/traces` 返回 404，错误信息却不是“服务挂了”。
- 25–75s：解释 v4 数据模型和 `events_only`：旧 traces/spans/generations/events ingestion 不再是当前写入路径。
- 75–125s：迁移方向：Python SDK v5、JS/TS SDK v6，底层基于 OpenTelemetry；也可使用 OTLP `/api/public/otel/v1/traces`。
- 125–160s：实时性注意：按当前官方兼容性文档核对 SDK/OTEL header，不能凭记忆猜 headers 或属性名。
- 160–180s：决策卡：先检查版本和迁移文档，再改代码；旧 endpoint 404 要记录为迁移信号。

## 证据

本地保存的官方文档快照说明：Python SDK v5、JS/TS SDK v6 采用 OpenTelemetry；自托管 v4 `events_only` 拒绝旧 ingestion；OTEL endpoint 可用于写入。当前实例现场探针也返回相同迁移提示。具体 SDK 参数、headers 和查询方式在录制当天按官方页面重新核对。

来源：<https://langfuse.com/docs/observability/sdk/overview>、<https://langfuse.com/docs/observability/sdk/upgrade-path>、<https://langfuse.com/integrations/native/opentelemetry>。

## 现场探针补充

当前实例的 OTEL 路径对 OPTIONS 返回 204，对空 JSON POST 返回 401；这只证明入口和认证门存在，不证明 Trace 已写入。真实演示必须用受保护项目 Key 和当前 SDK/OTEL exporter 发送脱敏 payload。

## 无凭据参考代码

`migration/python_v5_trace.py` 是从本地保存的官方 Python SDK v5 文档抽出的参考形状，已通过 Python 语法检查，但没有在当前环境运行；只有受保护凭据、锁定版本和新 Trace 回读齐全后才可升级证据等级。
