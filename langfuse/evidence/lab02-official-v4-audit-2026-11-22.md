# LAB-02 官方 Langfuse v4 迁移核验（2026-11-22）

## 结论

截至 2026-11-22（Asia/Shanghai），官方文档入口可访问，且与本轮 LAB-02 的迁移方向一致：Langfuse v4 的自定义 OTEL 写入使用 OTLP/HTTP，Trace endpoint 为 `/api/public/otel/v1/traces`；v4-ready 请求需要项目 Basic Auth 和 `x-langfuse-ingestion-version: 4`。本地探针只证明当前实例的旧路径返回迁移提示、OTEL 路径的认证门存在，未证明凭据认证、Trace 写入、Trace ID 回读或实时性。

## 官方页面核验

| 页面 | HTTP | 本次核对到的可引用事实 | 本地课程可用范围 |
|---|---:|---|---|
| [`Migrate ingestion to v4`](https://langfuse.com/integrations/native/opentelemetry/migration-to-v4) | 200 | v4-ready OTEL 通过 `/api/public/otel/v1/traces`；使用项目 Basic Auth，并发送 `x-langfuse-ingestion-version: 4`；每个操作应作为完整 OTEL span 导出 | 可支撑 LF-16/LF-19 的迁移方向和请求前置条件；不能替代本地写入证据 |
| [`OpenTelemetry`](https://langfuse.com/integrations/native/opentelemetry) | 200 | OTLP endpoint 为 `/api/public/otel`；信号专用 traces endpoint 为 `/api/public/otel/v1/traces`；支持 HTTP/JSON 与 HTTP/protobuf，不支持 gRPC；缺 v4 header 时直发 OTEL 数据可能延迟最多 10 分钟 | 可支撑 LF-20 的 endpoint、header、协议和实时性边界；不能把文档中的延迟上限当成本地 SLA |
| [`SDK upgrade path`](https://langfuse.com/docs/observability/sdk/upgrade-path) | 200 | 当前升级路径为 Python v4→v5、JS/TS v5→v6 | 可支撑版本核对清单；不能证明当前工作区安装或运行了这些版本 |
| [`SDK overview`](https://langfuse.com/docs/observability/sdk/overview) | 200 | Python SDK v5 与 JS/TS SDK v6 面向 Langfuse v4；其他语言可使用 OpenTelemetry | 可支撑 SDK/OTEL 选型；不能证明本轮受保护运行已发生 |

页面以同名 `.md` 内容端点复核，避免把动态页面的渲染状态当作 API 或实例结果。官方页面返回 200 只证明文档可访问，不证明字段、版本兼容性或当前实例行为；录制当天仍需复核。

## endpoint 口径

官方迁移指南讨论的 legacy ingestion endpoint 是 `/api/public/ingestion`；本轮现场探针记录的旧回读路径是 `/api/public/traces` 和 `/api/public/observations`。两者不能在旁白或证据表中合并称为同一个“旧 API”。当前实例返回的 `events_only` 迁移提示可以作为本地迁移信号；它不能单独推导所有旧 ingestion、回读或 SDK 路径的响应行为。

## 证据分层与当前状态

| claim | 证据 | 状态 |
|---|---|---|
| 官方 v4 OTEL endpoint、Basic Auth、`x-langfuse-ingestion-version: 4` | 上述官方迁移/OTEL 文档 | `documented` |
| 当前实例旧 `/traces`、`/observations` 返回 `events_only` 迁移提示 | [`lab02-live-probe-2026-11-22.md`](lab02-live-probe-2026-11-22.md) 与 raw 响应 | `verified`（仅响应范围） |
| 当前实例 OTEL 路径可达并要求认证 | [`lf16-otel-endpoint-probe-2026-11-22.md`](lf16-otel-endpoint-probe-2026-11-22.md) 的 405/204/401 | `verified`（仅探针范围） |
| 有效项目凭据认证、v4 Trace 写入、同一 Trace ID 回读 | 未执行受保护运行 | `BLOCKED` |
| flush 后实时可见及具体延迟 | 缺少 send/flush/readback 多组时间戳 | `BLOCKED` |

因此 LAB-02 总判定仍为 `health/readiness = sampled-pass`、`migration-signal = verified`、`new-trace-e2e = blocked`；LF-16、LF-19、LF-20 继续保持 `prototype / L1`。

## 复核命令

```bash
for u in \
  https://langfuse.com/integrations/native/opentelemetry/migration-to-v4.md \
  https://langfuse.com/integrations/native/opentelemetry.md \
  https://langfuse.com/docs/observability/sdk/upgrade-path.md \
  https://langfuse.com/docs/observability/sdk/overview.md; do
  curl -L -sS --max-time 20 -o /tmp/langfuse-official.md \
    -w 'url=%{url_effective} http=%{http_code} bytes=%{size_download}\n' "$u"
done
```

该命令只复核文档入口可访问性；它不发送项目数据，也不替代受保护 OTEL 证据包。
