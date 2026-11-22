# LF-20 事实审计：OTEL headers、时间戳与实时性

任务：LF20-S1。官方文档核对日期：2026-11-23（Asia/Shanghai）；仓库 OTEL 探针记录为 2026-11-22，本次未重新请求内网实例。

## 结论

这集要守住一句话：**请求到达 OTEL 入口，不等于事件带着正确认证、时间戳和资源信息落库并实时可见。headers、timestamp、flush、readback 要放进同一条证据链。**

- headers 决定能否进门、走哪条 ingestion 路径；缺 v4 header 会显著影响实时性。
- 时间戳缺失或不可解析时，Langfuse 会在 ingest 时补齐，可能把观测写成零时长或 ingest 时间。
- SDK/exporter 常批量发送；进程马上退出而没有 flush/shutdown，事件可能还在内存里。
- 当前没有项目 key，真实 payload、实时可见性、flush、重试回读全部未验证。状态保持 `prototype / L1`。

## headers 与实时性（官方口径）

来源：<https://langfuse.com/integrations/native/opentelemetry>（2026-11-23 读取）

| 项 | 官方口径 | 不能推出 |
|---|---|---|
| endpoint | OTLP `/api/public/otel`，信号专用 traces 入口 `/api/public/otel/v1/traces` | 入口可达就等于落库 |
| 认证 | 项目 Basic Auth | 401 以外的状态码分布 |
| v4 header | `x-langfuse-ingestion-version: 4` 让新数据实时进入 v4 数据模型 | 只加 header 就把旧格式变 v4-ready |
| 缺 header 的延迟 | 直发 OTEL 数据缺此 header 时可能延迟最多 10 分钟 | 这是本地实测 SLA |

“最多 10 分钟”是官方文档描述，不是本实例的延迟实测；不能当成本地 SLA 口播。

## 时间戳与 ingest 变换（官方口径）

同一官方页面的 ingestion transformations 说明：

- `startTimeUnixNano` 或 `endTimeUnixNano` 缺失/不可解析时，Langfuse 会复制另一端，让该观测变成零时长；两者都缺失时，都变成 ingest 时间。
- 每个 span 都应同时发送 start 和 end 两个字段。
- 若观测类型或时间戳看起来不对，可能是 Langfuse 在 ingest 时改写过的。

所以“时间戳有格式”不是装饰：它直接决定时长和排序是否可信。

## flush、批处理与重试

- SDK/exporter 常批量发送；进程立即退出而没有 flush/shutdown，内存中的事件可能尚未发出。
- 网络抖动时重试会带来延迟和重复风险。
- 演示要记录发送时间、首次响应、flush/shutdown 时间、重试次数，以及最终是否拿到 Trace ID；这些不齐，就不能把“本地调用结束”说成“服务端已保存”。

## 实时性要测量，不靠感觉

“马上可见”是一个可测量的延迟：从客户端发送或收到响应，到服务端回读成功的时间差。要设采样窗口、重复多次、记录每次时间戳，再谈 p50 或稳定性。单次截图只说明那一刻看到了，不代表实时性稳定。

证据表字段：`sent_at`、`response_at`、`readback_at`、`visibility_delay_ms`、`attempt`。

## 与现有 LF-20 课稿的对齐

`lf20-otel-headers-realtime-lesson.md` 的方向与本审计一致：headers/timestamp/flush/readback 四段、实时性要测量、当前只有认证门探针。需要补强的两点：

- 把官方“缺 v4 header 可能延迟最多 10 分钟”讲出来，作为实时性的具体抓手。
- 把官方 ingest 时间戳补齐规则讲出来，作为“时间戳为什么重要”的具体抓手。

## 与其他 agent 的冲突

- 若有人把“缺 header 最多延迟 10 分钟”说成本地实测 SLA，与本审计冲突；那是官方文档口径。
- 若有人把 OTEL 401、单次截图当成实时性证据，与本审计冲突。
- 若有人凭记忆口播时间戳/属性名而不核对官方页面，与课稿自身边界冲突。

## 需要冻结的字段

- 状态：`prototype / L1`；真实写入与实时性 `BLOCKED`。
- 四词主线：headers、timestamp、flush、readback。
- 实时性证据字段：sent_at、response_at、readback_at、visibility_delay_ms、attempt。
- 时间戳必须同时带 start 和 end。
- 禁出现：内网地址、真实 key / secret、Authorization 值、登录信息、PII。

## 依据

官方页面，2026-11-23 以 Markdown 端点读取：

- OTEL 集成（实时 ingestion、ingestion transformations、时间戳）：<https://langfuse.com/integrations/native/opentelemetry>
- 迁移指南：<https://langfuse.com/integrations/native/opentelemetry/migration-to-v4>

仓库内证据：

- `langfuse/lf20-otel-headers-realtime-lesson.md`
- `langfuse/evidence/lf16-otel-endpoint-probe-2026-11-22.md`
- `langfuse/evidence/lab02-official-v4-audit-2026-11-22.md`
- `langfuse/lf16-v4-otel-migration-fact-audit.md`
- `langfuse/lf19-otel-auth-readback-fact-audit.md`

## 产物与验证

独占产物：本文件。未改视频、字幕、播放器、manifest 或 `docs/quality/00-project-state.md`，未 git commit。

## 风险、缺口与未完成

- 没有项目 key，真实 headers、payload、flush、重试、实时性全部未验证。
- 采样来自 2026-11-22，本次未重新请求实例。
- “最多 10 分钟”是官方口径，不是本地实测。

## 建议下一步

由主 agent 把 LF-20 口播补上官方两个具体抓手（缺 header 的 10 分钟延迟、ingest 时间戳补齐规则）。等级升级只能等受保护写入、flush/shutdown 日志与多次回读延迟测量。
