# LF-19 事实审计：OTEL 认证门与 Trace 回读

任务：LF19-S1。官方文档核对日期：2026-11-23（Asia/Shanghai）；仓库 OTEL 探针记录为 2026-11-22，本次未重新请求内网实例。

## 结论

这集要守住一句话：**401 只证明入口存在且要求认证；只有拿到受保护写入的响应、Trace ID，并用同一 ID 回读核对，才能说“链路跑通”。**

- 401 的含义到“凭据缺失或不合法”为止，不是写入失败，也不是写入成功。
- 三级证据要分清：`sampled-pass`（入口探针）→ `write-observed`（认证后的写入响应）→ `e2e-verified`（带 Trace ID 的回读）。
- 当前环境没有项目 key，本集不执行真实写入、不伪造 Trace ID、不把 401 当成功。状态保持 `prototype / L1`。

## 401 认证门的边界

仓库 `evidence/lf16-otel-endpoint-probe-2026-11-22.md` 的探针结果：

| 请求 | 响应 | 能证明 | 不能证明 |
|---|---|---|---|
| HEAD `/api/public/otel/v1/traces` | 405 | 入口存在，不接受 HEAD | 写入成功 |
| OPTIONS 同路径 | 204 | 可预检响应 | 写入成功 |
| POST 空 JSON `{}` | 401 `Invalid credentials` | 路径可达、服务识别请求、认证门生效、凭据缺失或不合法 | payload 被接收、Worker 消费、UI 可查 Trace |

401 应被标成“认证门”，不是“失败写入”，更不是“成功写入”。它连 payload 是否被接收都不能说明。

## 最小证据闭环（四份证据）

要把“请求发出去了”升级成“链路跑通”，至少要留下：

1. 固定的 SDK 或 OTEL exporter 版本。
2. 受保护的项目 key 发送的脱敏 payload。
3. HTTP 状态、响应，以及返回或生成的 Trace ID。
4. 用相同实例和时间窗回读，核对服务端的 Trace、Observation 或等价事件。

少了第四步回读，最多只能算 `write-observed`。公开视频里 key 只留占位符（`LANGFUSE_PUBLIC_KEY`、`LANGFUSE_SECRET_KEY`、`TRACE_ID`），不录真实密钥、用户输入、模型原文或内网地址。

## 回读路径

- 旧 `/api/public/traces`、`/api/public/observations` 在 v4 `events_only` 下返回迁移提示，不能再当回读验收命令。
- 回读应使用当前 v4 支持的查询方式：官方 UI，或当前 API / CLI（`npx @langfuse/cli api <resource> <action>`，由 OpenAPI spec 生成，覆盖 traces、observations、scores 等）。
- 具体端点路径、参数和响应字段以录制当天的 API reference 为准；本审计不臆造 v4 回读端点。

## 三级证据与当前状态

| 等级 | 含义 | 当前是否达到 |
|---|---|---|
| `sampled-pass` | 入口探针：路由存在、认证门生效 | 已达（仅探针范围） |
| `write-observed` | 认证后的写入响应、Trace ID | 未达，BLOCKED |
| `e2e-verified` | 同一 Trace ID 的回读核对 | 未达，BLOCKED |

当前环境停在第一层认证探针，真实 E2E 为 `BLOCKED`。

## 与现有 LF-19 课稿的对齐

`lf19-otel-auth-readback-lesson.md` 的方向与本审计一致：区分入口存在 / 认证通过 / 写入可回读；把 401 标成认证门；用三级证据收束。需要保留的收紧点：

- 回读一步不要指向旧 traces/observations 路径；用当前 v4 UI 或 API/CLI。
- `write-observed` 与 `e2e-verified` 之间必须隔着同一 Trace ID 的回读，不能合并。
- 演示模板里的环境变量只能是占位符。

## 与其他 agent 的冲突

- 若有人把 OTEL 401、OPTIONS 204 当成“Trace 上报成功”，与本审计冲突。
- 若有人用旧 traces/observations 路径做回读验收，与 v4 `events_only` 迁移提示冲突。
- 若有人把入口探针（sampled-pass）当成 e2e-verified，与三级证据定义冲突。

## 需要冻结的字段

- 状态：`prototype / L1`；`new-trace-e2e = blocked`。
- 三级证据：sampled-pass → write-observed → e2e-verified。
- 证据模板字段：`sdk_version`、`endpoint`、`payload_hash`、`http_status`、`trace_id`、`readback_status`、`captured_at`。
- 回读用当前 v4 UI / API / CLI，不用旧路径。
- 禁出现：内网地址、真实 key / secret、Authorization 值、登录信息、PII。

## 依据

官方页面，2026-11-23 以 Markdown 端点读取：

- OTEL 集成（认证、header、endpoint）：<https://langfuse.com/integrations/native/opentelemetry>
- 迁移指南：<https://langfuse.com/integrations/native/opentelemetry/migration-to-v4>
- CLI（v4 查询方式）：<https://langfuse.com/docs/api-and-data-platform/features/cli>
- API reference：<https://api.reference.langfuse.com>

仓库内证据：

- `langfuse/lf19-otel-auth-readback-lesson.md`
- `langfuse/evidence/lf16-otel-endpoint-probe-2026-11-22.md`
- `langfuse/evidence/lf19-evidence-audit-2026-11-22.md`
- `langfuse/evidence/lab02-live-probe-2026-11-22.md`
- `langfuse/lf16-v4-otel-migration-fact-audit.md`

## 产物与验证

独占产物：本文件。未改视频、字幕、播放器、manifest 或 `docs/quality/00-project-state.md`，未 git commit。

## 风险、缺口与未完成

- 没有项目 key，真实认证、写入、Trace ID、回读全部未验证。
- 采样来自 2026-11-22，本次未重新请求实例。
- v4 回读端点的具体参数需在录制当天核对 API reference，本审计不臆造。

## 建议下一步

由主 agent 把 LF-19 口播按本审计收紧：回读走当前 v4 UI/API/CLI，保留三级证据与 401 边界。等级升级只能等受保护写入与同一 Trace ID 回读证据，逐级提升，不能直接从 L1 改成 verified。
