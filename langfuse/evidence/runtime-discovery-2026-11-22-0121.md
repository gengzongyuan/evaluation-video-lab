# LAB-02 runtime discovery（2026-11-22 01:21 Asia/Shanghai）

## 目的

对当前自托管 Langfuse v4 节点进行一次只读复核，确认既有环境契约中的 Web、Gateway、MinIO 和 OTEL 端点结论是否仍与现场响应一致。本轮不包含项目 key，不提交业务 Trace、Score 或 Dataset。

## 采样结果

| 端点 | HTTP | 响应摘要 | 判定 |
|---|---:|---|---|
| `http://172.16.33.136:3000/api/public/health?failIfDatabaseUnavailable=true` | 200 | `{"status":"OK","version":"4.79.0"}` | sampled-pass |
| `http://172.16.33.136:3000/api/public/ready` | 200 | `{"status":"OK","version":"4.79.0"}` | sampled-pass |
| `http://172.16.33.136:3031/health` | 200 | `{"status":"ok"}` | sampled-pass |
| `http://172.16.33.136:3031/ready` | 503 | `{"status":"unconfigured"}` | blocked/risk |
| `http://172.16.33.136:9090/minio/health/live` | 200 | 空正文 | sampled-pass |
| `POST http://172.16.33.136:3000/api/public/otel/v1/traces`（空 JSON） | 401 | `Invalid credentials` / `UnauthorizedError` | auth gate observed |

补充方法探针：OTEL `HEAD` 返回 405，`OPTIONS` 返回 204，说明入口路由存在并按方法/认证处理请求；这两项不构成写入成功。

## 与既有契约的一致性

本轮响应与 [`lab02-environment-contract.md`](../../docs/quality/lab02-environment-contract.md) 及 00:44 采样结论一致：Web health/ready 与 Gateway health 在采样时通过，Gateway readiness 仍未配置，OTEL 入口仍要求有效认证，实例版本仍为 4.79.0。未发现足以升级 `new-trace-e2e` 的证据。

## 证据与完整性

本轮原始正文保存在 `raw/`：

- `lab02-health-2026-11-22-0121.json`
- `lab02-web-ready-2026-11-22-0121.json`
- `lab02-gateway-health-2026-11-22-0121.json`
- `lab02-gateway-ready-2026-11-22-0121.json`
- `lab02-minio-live-2026-11-22-0121.txt`
- `lab02-otel-head-2026-11-22-0121.txt`
- `lab02-otel-options-2026-11-22-0121.txt`
- `lab02-otel-post-2026-11-22-0121.json`

对应 SHA-256 清单：`raw/SHA256SUMS-2026-11-22-0121.txt`。

## 边界

这只是新的时间点只读采样。它不能证明 OTEL 认证成功、Trace ingestion、Worker 消费、当前 UI/API 回读、Gateway 模型请求、重启恢复、成本或稳定性。项目 key/secret 未在 shell 中出现，也未写入证据。
