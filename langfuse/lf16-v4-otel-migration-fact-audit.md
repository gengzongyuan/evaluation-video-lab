# LF-16 事实审计：Langfuse v4 与 OTEL 迁移

任务：LF16-S1。官方文档核对日期：2026-11-23（Asia/Shanghai）；仓库现场探针记录为 2026-11-22，本次未重新请求内网实例。

## 结论

这集要讲清楚的是：**旧路径返回迁移信号，不等于新链路已经跑通；迁移的验收必须落到一次受保护写入后的同一 Trace ID 回读。**

- Langfuse v4 的 `events_only` 提示说明旧 ingestion / 回读路径不再是当前写入主路径，应升级到当前 SDK 或使用 OpenTelemetry。
- 官方迁移方向：Python SDK v5、JS/TS SDK v6 面向 Langfuse v4；自定义或其他语言集成可用 OTLP/HTTP 发到 OTEL traces 入口。
- OTEL 入口存在、返回 204/401、health 200，都不能证明 Trace 已写入、Worker 已消费或回读成功。
- 本任务没有项目 key，没有执行受保护写入。状态保持 `prototype / L1`。

## events_only 与 OTEL 的关系

| 概念 | 可以怎么讲 | 不能推出 |
|---|---|---|
| v4 `events_only` | 自托管 v4 的旧 `/api/public/traces`、`/api/public/observations` 路径返回迁移提示；官方自定义迁移指南讨论的 legacy 入口是 `/api/public/ingestion` | 所有旧 SDK、所有旧查询路径、所有实例返回完全一致 |
| 迁移目标 | 升级到当前 SDK，或把自定义/已有 OTEL 管道改成 v4-ready 的 OTEL span | 只改一个 URL 就完成迁移 |
| OTEL 入口 | `/api/public/otel/v1/traces`，OTLP over HTTP | 入口可达就等于数据已落库 |
| v4-ready 请求 | 项目 Basic Auth，加 `x-langfuse-ingestion-version: 4`；每个操作是一条完整 span，带合法 trace ID、span ID、时间和 parent context | 只加 header 就把旧格式变成 v4-ready |

两个“旧 API”不能混为一谈：迁移文档讲的 legacy ingestion endpoint 是 `/api/public/ingestion`；本轮现场探针请求的是 `/api/public/traces` 和 `/api/public/observations`。旁白和证据表应分别标注，不要统称“旧 API 都返回 404”。

## 成功迁移需要的证据

一次可复核的迁移演示至少要留下：

1. 锁定的 SDK 或 OTEL exporter 版本，以及服务端版本。
2. 受保护的项目凭据来源，画面中只出现占位符。
3. OTEL endpoint、`x-langfuse-ingestion-version: 4`、Content-Type、编码方式，以及脱敏后的最小 payload。
4. 发送响应、Trace ID，以及短生命周期进程的 flush / shutdown 记录。
5. 用当前 v4 支持的 UI 或 API 读取同一条 Trace / Observation，核对名称、父子关系、时间戳和输入输出。
6. 采样时间、运行 commit 和回读时间，避免把历史记录当成本次新运行。

官方 SDK 概览建议 Python / JS/TS 优先用 SDK，让 SDK 处理属性、上下文传播、媒体、过滤和导出；其他语言可用原生 OTEL API。缺 `x-langfuse-ingestion-version: 4` 时，直发 OTEL 的数据在官方文档里被描述为可能延迟最多 10 分钟；这是文档口径，不是本地 SLA 实测。

## 现场探针能证明和不能证明的范围

以下只引用仓库里已有的探针记录，本次没有重新发请求：

| 观察 | 证据 | 状态 | 不能推出 |
|---|---|---|---|
| 旧 traces / observations 路径返回 v4 `events_only` 迁移提示 | `evidence/lab02-live-probe-2026-11-22.md` 及 raw 响应 | verified（仅响应范围） | 新 Trace 已写入 |
| OTEL traces 路径 HEAD 405、OPTIONS 204、空 JSON POST 401 | `evidence/lf16-otel-endpoint-probe-2026-11-22.md` | verified（仅探针范围） | 有效认证、payload 被接收、Worker 消费、回读成功 |
| health 返回版本 4.79.0 | 同一探针记录 | 时间点采样 | 当前部署此刻仍健康、OTEL 链路已验收 |
| 受保护凭据下的真实 OTLP 写入与同一 Trace ID 回读 | 未执行 | BLOCKED | — |

401 的含义只到“入口要求有效认证、凭据缺失或不合法”。204 只说明预检响应。health 200 只说明那个时间点的健康检查。三者都不是写入成功证据。

## 与现有 LF-16 课稿的对齐

`lf16-v4-otel-migration-lesson.md` 的方向与本审计一致：识别 `events_only`、走 SDK v5 / JS v6 或 OTEL、把 404/401 标成迁移信号而不是服务宕机。需要保留的收紧点：

- 不要把“官方页面 200”说成“当前实例已验证”。
- 不要把 OTEL 入口 401/204 说成“Trace 上报成功”。
- 不要把无凭据参考代码 `migration/python_v5_trace.py` 说成已运行；它只过了语法检查。
- 具体 SDK 参数、headers、查询方式在录制当天重新核对官方页面。

## 与其他 agent 的冲突

- 若有人把 v3 媒体门 PASS、Xiaoxiao 旁白、画面内字幕当成 LF-16 已验证，与本审计冲突；那是制作质量，不是运行证据。
- 若有人把 OTEL 401、health 200 或历史 Trace 截图当成新链路跑通，与本审计冲突。
- 若有人把 `/api/public/ingestion` 和 `/api/public/traces` 合并成同一个“旧 API”，以本文件的区分为准。

## 需要冻结的字段

- 状态：`prototype / L1`；`new-trace-e2e = blocked`。
- 迁移主线：Python SDK v5、JS/TS SDK v6，或 OTEL/OTLP。
- 入口：`/api/public/otel/v1/traces`；header `x-langfuse-ingestion-version: 4`；项目 Basic Auth。
- 证据闭环：版本 → 受保护凭据 → 脱敏 payload → 响应与 Trace ID → flush/shutdown → 同一 ID 回读。
- 禁出现：内网地址、真实 key / secret、Authorization 值、登录信息、PII。

## 依据

官方页面，2026-11-23 以 Markdown 端点读取：

- 迁移指南：<https://langfuse.com/integrations/native/opentelemetry/migration-to-v4>
- OTEL 集成：<https://langfuse.com/integrations/native/opentelemetry>
- SDK 概览：<https://langfuse.com/docs/observability/sdk/overview>
- SDK 升级路径：<https://langfuse.com/docs/observability/sdk/upgrade-path>
- Python v4 → v5：<https://langfuse.com/docs/observability/sdk/upgrade-path/python-v4-to-v5>

仓库内证据：

- `langfuse/lf16-v4-otel-migration-lesson.md`
- `langfuse/migration/README.md`
- `langfuse/evidence/lab02-official-v4-audit-2026-11-22.md`
- `langfuse/evidence/lab02-live-probe-2026-11-22.md`
- `langfuse/evidence/lf16-otel-endpoint-probe-2026-11-22.md`
- `langfuse/lf14-version-pinning-fact-audit.md`

## 产物与验证

独占产物：本文件。未改视频、字幕、播放器、manifest 或 `docs/quality/00-project-state.md`，未 git commit。

## 风险、缺口与未完成

- 没有项目 key，真实 OTEL 写入、Worker 消费、回读、flush 实时性全部未验证。
- 当前实例只来自历史探针，本次未重新采样。
- 旧 SDK 的具体代码改动量取决于项目现状，本审计不声称任何项目已升级完成。

## 建议下一步

由主 agent 把 LF-16 口播按本审计收紧，保留“迁移信号 ≠ 链路已验收”的边界；真正的等级升级只能等受保护的 OTEL 写入与同一 Trace ID 回读证据。
