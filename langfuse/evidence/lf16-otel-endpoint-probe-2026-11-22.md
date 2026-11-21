# LF-16 OTEL 入口探针（2026-11-22）

## 目的

确认当前 Langfuse v4 实例的 OTEL 入口是否存在、是否要求认证；不发送业务 Trace，不使用项目 Key。

## 结果

| 请求 | 响应 | 解释 |
|---|---:|---|
| `HEAD /api/public/otel/v1/traces` | 405 | 入口存在，但不接受 HEAD 方法 |
| `OPTIONS /api/public/otel/v1/traces` | 204 | 入口可进行预检响应 |
| `POST /api/public/otel/v1/traces`，空 JSON `{}` | 401 | 入口要求有效认证；未写入业务数据 |

401 响应摘要：`Invalid credentials. Confirm that you've configured the correct host.`

## 结论边界

- PASS：当前实例暴露 OTEL 路径，且认证门生效。
- BLOCKED：没有项目 Key，因此没有发送真实 OTLP payload，不能证明 Trace 写入、UI/API 回读或字段映射成功。
- 不可宣称：不能把 204/401 当成“Trace 已成功上报”；下一步必须用受保护 Key、当前 SDK/OTEL exporter 和脱敏最小 Trace 完成端到端验证。
