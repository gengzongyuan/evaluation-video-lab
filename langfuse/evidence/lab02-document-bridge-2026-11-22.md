# LAB-02 证据桥接记录（2026-11-22）

## 用途

把同一轮 LAB-02 的三类只读证据接到课程记录，避免把服务健康、迁移入口和真实 Trace 写入混成一个结论。本文只做证据索引和边界声明，不提高任何视频或实验的证据等级。

## 证据关系

| 事实层 | 当前证据 | 能证明 | 不能证明 |
|---|---|---|---|
| Web 健康与 readiness | `evidence/runtime-discovery-2026-11-22-0044.md` 及其 `raw/` 正文 | 2026-11-22 00:44 采样时 Web `/health`、`/ready` 返回 200，版本为 4.79.0 | OTEL 写入、Worker 消费、UI/API 回读、重启恢复 |
| Gateway 与对象存储采样 | 同上 | Gateway `/health` 返回 200，MinIO liveness 返回 200 | Gateway `/ready` 可用；该项实际为 503 `unconfigured` |
| v4 迁移信号 | `evidence/lab02-live-probe-2026-11-22.md`、`evidence/lf16-otel-endpoint-probe-2026-11-22.md` | 旧 Trace/Observation 路径返回 v4 `events_only` 迁移提示；OTEL 路径存在且要求认证 | 真实 OTLP payload 已写入或能在 UI/API 回读 |
| 历史调用树 | `evidence/historical-lab02-observation-summary.md` | 可用于解释 Trace/Observation 概念 | 当前 4.79.0 实例的新运行结果 |

## 给 LF-02 / LF-16 / LF-17 的使用规则

- LF-02 可引用历史调用树讲概念；当前实例状态应引用现场探针和 00:44 runtime discovery，并保持“新 Trace 未验证”。
- LF-16 可引用旧 endpoint 的 404 迁移提示和 OTEL 入口 401 认证门；401 只说明入口要求凭据，不是写入成功。
- LF-17 可引用 00:44 的分层状态：Web health/ready 通过、Gateway health 通过、Gateway ready 为 `503 unconfigured`、MinIO liveness 通过；这是一组时间点采样，不是完整链路验收。

## 统一放行判断

当前 LAB-02：`health/readiness = sampled-pass`，`migration-signal = verified`，`new-trace-e2e = blocked`。在受保护项目 Key、锁定 SDK/OTEL 版本、脱敏 payload、Trace ID 回读和原始响应齐全前，LF-02–LF-17 保持 `prototype / L1`，不得写成当前实例已成功上报 Trace。

## 原始证据索引

- `evidence/raw/lab02-health-2026-11-22-0044.json`
- `evidence/raw/lab02-web-ready-2026-11-22-0044.json`
- `evidence/raw/lab02-gateway-health-2026-11-22-0044.json`
- `evidence/raw/lab02-gateway-ready-2026-11-22-0044.json`
- `evidence/raw/lab02-minio-live-2026-11-22-0044.txt`
- `evidence/raw/lab02-health-2026-11-22.json`
- `evidence/raw/lab02-legacy-traces-endpoint-2026-11-22.json`
- `evidence/raw/lab02-legacy-observations-endpoint-2026-11-22.json`

所有原始响应均为脱敏的只读探针输出；不包含项目 key 或 secret。
