# LF-20：OTEL headers、时间戳与实时性

- **时长**：约 180 秒
- **级别**：迁移 / 生产
- **状态**：`prototype / L1`
- **一句话结果**：请求能到达 OTEL 入口，不等于事件已经带着正确认证、时间戳和资源信息落库；录制时要把 headers、时间戳、flush/重试与回读放进同一条证据链。
- **当前边界**：仓库没有项目 key，无法在当前实例验证真实 OTEL payload、实时可见性、flush 或重试后的回读；以下是官方文档导向的录制设计，不是运行结果。

## 180 秒时间轴

### 0–20 秒：开场钩子

**口播**：

> 为什么同一个 OTEL 请求，有时返回 401，有时请求成功却暂时看不到 Trace？因为“请求发出”中间还有认证、时间戳、资源属性和异步发送。今天只记四个词：headers、timestamp、flush、readback。

**画面**：四张卡片依次出现，右下角固定 `prototype / L1`。

### 20–60 秒：headers 先决定能不能进门

**口播**：

> OTLP HTTP 请求至少要按当前官方文档确认 endpoint、认证 headers、Content-Type 和编码方式。不要从旧 SDK 代码复制一行就当成 v4 通用答案。录制时把 header 名称和版本写进证据表，真实 secret 只来自受保护环境变量，画面中只展示占位符。

**画面**：伪代码卡片：`OTEL_EXPORTER_OTLP_ENDPOINT`、`Authorization: <redacted>`、`Content-Type`；把版本号和来源链接放在旁边。

### 60–100 秒：时间戳与资源信息

**口播**：

> 一个事件至少要能解释“什么时候发生、由谁产生”。时间戳、service name、environment 和 trace/span 关系会影响查询、排序和归因。时间戳格式、属性名和 exporter 默认值必须以录制当天的官方文档为准；不确定就把字段标为待核对，不要凭记忆口播。

**画面**：脱敏 payload 结构图，标出 `time`、`trace_id`、`span_id`、`service.name`、`deployment.environment`，每个字段注明“示意，需按当前版本核对”。

### 100–140 秒：flush、批处理和重试

**口播**：

> SDK 或 exporter 常会批量发送。进程马上退出时，如果没有 flush 或 shutdown，内存里的事件可能还没发出去。网络抖动时，重试会带来延迟和重复风险。演示要记录发送时间、首次响应、flush 或 shutdown 时间、重试次数，以及最终是否拿到 Trace ID；这些字段没有齐，就不能把“本地调用结束”说成“服务端已保存”。

**画面**：时间线：`create span → export queued → flush/shutdown → HTTP response → readback`；失败分支标注 `retry`。

### 140–165 秒：实时性不是凭感觉

**口播**：

> “马上可见”是一个可测量的延迟：从客户端发送或收到响应，到服务端回读成功的时间差。要设定采样窗口，重复多次，并记录 p50 或至少每次的时间戳。单次截图只能说明那一刻看到了，不代表实时性稳定。

**画面**：证据表列 `sent_at`、`response_at`、`readback_at`、`visibility_delay_ms`、`attempt`。

### 165–180 秒：收束与 CTA

**口播**：

> 下一次录制前，先核对四件事：headers 有来源，时间戳有格式，flush 和重试有日志，Trace ID 能回读。当前环境只有认证门探针，真实写入和实时性保持 BLOCKED；补齐凭据后，再把这集升级为可验证版本。

**画面**：四项清单与 `BLOCKED until protected write + readback`。

## 演示步骤

1. 打开仓库中记录的官方来源审计，确认 endpoint、headers 和 SDK 版本以当前页面为准。
2. 展示脱敏 OTLP 请求模板；所有 key、secret、用户输入和内网地址使用占位符。
3. 展示包含时间戳、trace/span 关联和资源属性的示意 payload，并标记“字段需按当前版本核对”。
4. 展示 exporter 批处理、flush/shutdown、重试和最终回读的日志字段；不要伪造响应或 Trace ID。
5. 有受保护项目 key 后，重复多次测量 `sent_at → readback_at`，保存状态码、响应、Trace ID 和时间窗。

## 证据分级

| 结论 | 当前状态 | 需要的证据 |
|---|---|---|
| OTEL 入口可达且有认证门 | `sampled-pass` / `verified`（探针范围） | `evidence/lf16-otel-endpoint-probe-2026-11-22.md` |
| headers 与 payload 被服务接受 | `BLOCKED` | 版本锁定、脱敏 payload、HTTP 响应和原始命令 |
| flush 后事件可回读 | `BLOCKED` | flush/shutdown 日志、Trace ID、回读响应 |
| 实时性达到某个延迟目标 | `BLOCKED` | 多次 `sent_at`/`readback_at` 和统计口径 |

## 参考与边界

- `langfuse/lf19-otel-auth-readback-lesson.md`
- `langfuse/lf16-v4-otel-migration-lesson.md`
- `langfuse/evidence/lf16-otel-endpoint-probe-2026-11-22.md`
- `langfuse/evidence/lab02-raw-integrity-2026-11-22.md`
- `langfuse/source-link-audit-2026-11-22.md`
- 具体 headers、属性名和 exporter 行为必须在录制当天重新核对 Langfuse 官方当前文档；本文件不把示意字段当成已运行事实。

## 发布前检查

- [ ] 约 180 秒，音频和视频流均存在。
- [ ] 字幕逐字复核 `headers`、`flush`、`retry`、`readback` 和 `BLOCKED`。
- [ ] 无真实 key、secret、PII、未脱敏 payload 或内网凭据。
- [ ] 若补齐真实运行，保存 SDK/OTEL 版本、headers 来源、状态码、Trace ID、flush/shutdown 日志和回读时间。
