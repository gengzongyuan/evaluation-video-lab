# LF-17 事实审计：Health / Readiness 验证

任务：LF17-S1。官方文档核对日期：2026-11-23（Asia/Shanghai）；仓库 runtime 采样记录为 2026-11-22，本次未重新请求内网实例。

## 结论

这集要守住一句话：**health 200、ready 200、Gateway health 200、MinIO liveness 200，分别只说明各自采样时那一个端点的状态；没有一个能证明新 Trace 已经写入、Worker 已消费或回读成功。**

- health 是“进程在跑”的信号；readiness 是“可以接流量”的信号；两者都不是业务写入验收。
- 官方 web `/api/public/health` 默认**不**校验数据库连通性，要加 `failIfDatabaseUnavailable=true` 才把数据库纳入检查。
- Worker 有独立健康端点 `/api/health`；Web 的 ready 通过不能替代 Worker 状态。
- 当前缺项目 key，真实 OTEL 写入、消费、回读、重启恢复、备份恢复全部未验证。状态保持 `prototype / L1`。

## 官方端点定义（2026-11-23 读取）

来源：<https://langfuse.com/self-hosting/configuration/health-readiness-endpoints>

| 容器 | 端点 | 官方口径 | 不能推出 |
|---|---|---|---|
| langfuse-web | `/api/public/health` | API 是否在运行；默认不查数据库 | 数据库可用、Trace 已写入 |
| langfuse-web | `/api/public/health?failIfDatabaseUnavailable=true` | 同上，且数据库可达 | Worker 消费、回读成功 |
| langfuse-web | `/api/public/ready` | 是否可接收流量；收到 SIGTERM/SIGINT 时返回 500 | 依赖全部就绪、业务链路已验收 |
| langfuse-worker | `/api/health` | Worker 服务与数据库连接是否正常 | 队列没有积压、某条 Trace 已处理 |

Worker 还有两个专用探针：`failIfEventPropagationStuck=true`（v3→v4 dual write 期间事件传播是否停滞）与 `failIfQueueConsumptionStuck=true`（队列消费是否停滞）。它们能补“Worker 假活”这一类盲区，但仍是 Worker 自身信号，不是某条 Trace 的端到端回读。

## 仓库现有采样能证明什么

以下只引用 `evidence/runtime-discovery-2026-11-22-0044.md` 的只读采样，本次没有重新发请求：

| 观察 | 状态 | 能证明 | 不能证明 |
|---|---|---|---|
| Web health（带数据库参数）200 | PASS（采样） | 采样时 API 与数据库健康 | Trace 写入、Worker 消费、回读 |
| Web ready 200 | PASS（采样） | 采样时可接流量 | 重启后仍 ready、备份可恢复 |
| Gateway health 200 | PASS（采样） | Gateway 进程在跑 | Gateway 请求链路已配置 |
| Gateway ready 503 `unconfigured` | RISK | 网关未配置，不能当作可用 | — |
| MinIO liveness 200 | PASS（采样） | 对象存储进程存活 | 读写正确、备份恢复 |

`unconfigured` 的 Gateway 是一个真实的反例：同一个部署里，进程 health 通过而 ready 失败。它适合拿来教“health ≠ ready ≠ 业务可用”，但不能被剪成“服务已就绪”。

## 与现有 LF-17 课稿的对齐

`lf17-health-readiness-lesson.md` 的方向与本审计一致：区分 health、readiness 和真实写入；用 Gateway ready 503 做反例；强调端点采样不等于全链路。需要保留的收紧点：

- 讲 health 时必须带上“默认不查数据库”这一限定，否则观众会误以为 200 已包含数据库。
- Web ready 200 不能替代 Worker `/api/health`；课稿若只画 Web/Gateway/MinIO，要补 Worker 这一层或明确标为未采样。
- 公开视频隐藏内网 IP、端口和服务拓扑细节。

## 与其他 agent 的冲突

- 若有人把 health/ready 200 或 MinIO liveness 200 当成 LF-17 已验证 Trace 链路，与本审计冲突。
- 若有人把 Gateway health 200 说成“网关已配置可用”，与 runtime 采样里的 ready 503 `unconfigured` 冲突，以后者为准。
- 若有人引用 `/self-hosting/health-checks` 作为来源，该路径不存在；正确路径是 `/self-hosting/configuration/health-readiness-endpoints`。

## 需要冻结的字段

- 状态：`prototype / L1`；`new-trace-e2e = blocked`。
- 分层：health（进程）→ readiness（接流量）→ Worker（独立健康）→ 真实写入与回读（业务验收）。
- health 的数据库参数：`failIfDatabaseUnavailable=true`。
- Gateway `unconfigured` 记为 RISK，不得放行。
- 禁出现：内网地址、真实 key / secret、Authorization 值、登录信息、PII。

## 依据

官方页面，2026-11-23 以 Markdown 端点读取：

- 健康与 readiness 端点：<https://langfuse.com/self-hosting/configuration/health-readiness-endpoints>
- 自托管概览：<https://langfuse.com/self-hosting>
- Docker Compose 部署（含 Gateway ready 503 说明）：<https://langfuse.com/self-hosting/deployment/docker-compose>

仓库内证据：

- `langfuse/lf17-health-readiness-lesson.md`
- `langfuse/evidence/runtime-discovery-2026-11-22-0044.md`
- `langfuse/lf13-fact-audit.md`
- `langfuse/lf16-v4-otel-migration-fact-audit.md`

## 产物与验证

独占产物：本文件。未改视频、字幕、播放器、manifest 或 `docs/quality/00-project-state.md`，未 git commit。

## 风险、缺口与未完成

- 采样来自 2026-11-22，本次未重新请求实例；当前此刻状态未知。
- Worker `/api/health` 未在该采样中体现，Worker 实际状态未验证。
- 没有项目 key，真实写入、消费、回读、重启恢复、备份恢复全部 BLOCKED。

## 建议下一步

由主 agent 把 LF-17 口播按本审计收紧：health 带数据库参数、Worker 单列、Gateway 503 作反例。真正的等级升级只能等受保护写入与同一 Trace ID 回读证据。
