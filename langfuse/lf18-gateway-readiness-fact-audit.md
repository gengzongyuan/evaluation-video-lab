# LF-18 事实审计：Gateway readiness

任务：LF18-S1。官方文档核对日期：2026-11-23（Asia/Shanghai）；仓库 Gateway 采样记录为 2026-11-22，本次未重新请求内网实例。

## 结论

这集要守住一句话：**Gateway `/health` 200 只说明进程在服务 HTTP；`/ready` 503 `unconfigured` 说明还没配好 web URL 和 service key。两者都不是“模型请求已打通”的证据。**

- `/health` 是 liveness，不检查依赖；`/ready` 是 readiness，配好配置后才 200。
- 官方明确：`/ready` 不会真的调用 web 或 provider，web/provider 不可达时 ready 仍可能 200。所以 ready 200 也不能证明模型请求链路可用。
- 当前 Langfuse Trace 写入不依赖 Gateway；但若模型请求链路走 Gateway，未 ready 时不能把模型请求、成本、延迟说成生产证据。
- 本次没有修改 Gateway 配置，没有发送模型请求。状态保持 `prototype / L1`。

## 官方端点定义（2026-11-23 读取）

来源：<https://langfuse.com/self-hosting/configuration/ai-gateway>（Health checks 一节）

| 端点 | 类型 | 官方口径 | 不能推出 |
|---|---|---|---|
| `/health` | Liveness | 进程在服务 HTTP 时返回 `200 {"status":"ok"}`，包括 shutdown 期间；不检查依赖 | web/provider 可达、配置就绪、模型请求可用 |
| `/ready` | Readiness | 配好 web URL 和 service key 后 `200 {"status":"ready"}`；缺配置时 `503 {"status":"unconfigured"}`；shutdown 时 `503 {"status":"draining"}` | web/provider 真实可达、单次模型请求成功 |

关键限定：`/ready` 不调用 web 或 provider，所以它们不可达时 ready 仍可能 200；这些失败只会出现在单次请求和网关日志里。`/ready` 适合给负载均衡器做健康检查，不适合当业务验收。

## unconfigured 的含义边界

- 官方配置表写明：缺 `LANGFUSE_AI_GATEWAY_WEB_URL` 时 `/ready` 返回 503 且推理被禁用。
- `LANGFUSE_AI_GATEWAY_ALLOW_MISSING_SERVICE_KEY=true` 时，web URL 已设但 service key 未设，会以 503 `/ready` 的未配置状态启动；Docker Compose 默认这样设置。
- 所以 `unconfigured` 指向“web URL / service key 这类配置缺失”，但它不是完整诊断：具体缺哪一项、provider 路由是否正确，仍需在受保护环境核对配置。
- 它是风险信号，不应被剪成“网关已就绪”。

## 仓库现有采样能证明什么

以下只引用 `evidence/runtime-discovery-2026-11-22-0044.md`、`runtime-discovery-2026-11-22-0121.md` 与 `evidence/lf18-gateway-probe.md`，本次没有重新发请求：

| 观察 | 状态 | 能证明 | 不能证明 |
|---|---|---|---|
| Gateway `/health` 200 | PASS（采样） | 采样时进程存活 | 配置就绪、模型请求可用 |
| Gateway `/ready` 503 `unconfigured` | RISK | 采样时未配置就绪 | 具体缺哪个 provider/service key、生产安全 |
| 两次采样结果一致 | 一致性 | 00:44 与 01:21 结论未变 | 此刻仍相同、重启恢复 |

探针没有修改配置、发送模型请求或写入 Trace。

## 与现有 LF-18 课稿的对齐

`lf18-gateway-readiness-lesson.md` 的方向与本审计一致：把进程存活、配置就绪、真实模型请求分三层；用 health 200 + ready 503 做钩子；强调 Trace 写入不依赖 Gateway。需要保留的收紧点：

- ready 503 要落到官方定义的配置项（web URL、service key），不要笼统说成“provider 或路由配置”。
- 明确 ready 不调用 web/provider，避免观众以为 ready 200 就证明链路通。
- 公开视频只保留状态，不展示内网 IP、密钥或 provider 配置。

## 与其他 agent 的冲突

- 若有人把 Gateway health 200 当成“网关已配置可用”，与 ready 503 `unconfigured` 冲突，以后者为准。
- 若有人把 ready 200 当成“模型请求已打通”，与官方“ready 不调用 web/provider”冲突。
- 若有人把本集当成 Langfuse Trace 写入验收，与本审计冲突；Trace 写入不依赖 Gateway。

## 需要冻结的字段

- 状态：`prototype / L1`；Gateway 未 ready 时模型链路相关结论保持 RISK/BLOCKED。
- 三层：liveness（进程）→ readiness（配置就绪）→ 真实模型请求（业务验收）。
- `unconfigured` = 配置未就绪（web URL / service key），不是完整诊断。
- ready 不调用 web/provider。
- 禁出现：内网地址、真实 key / secret、Authorization 值、登录信息、PII。

## 依据

官方页面，2026-11-23 以 Markdown 端点读取：

- AI Gateway（含 Health checks、配置表、ready 行为）：<https://langfuse.com/self-hosting/configuration/ai-gateway>
- Docker Compose 部署（Gateway ready 503 说明）：<https://langfuse.com/self-hosting/deployment/docker-compose>

仓库内证据：

- `langfuse/lf18-gateway-readiness-lesson.md`
- `langfuse/evidence/lf18-gateway-probe.md`
- `langfuse/evidence/runtime-discovery-2026-11-22-0044.md`
- `langfuse/evidence/runtime-discovery-2026-11-22-0121.md`
- `langfuse/lf17-health-readiness-fact-audit.md`

## 产物与验证

独占产物：本文件。未改视频、字幕、播放器、manifest 或 `docs/quality/00-project-state.md`，未 git commit。

## 风险、缺口与未完成

- 采样来自 2026-11-22，本次未重新请求实例；当前此刻 Gateway 状态未知。
- 没有修改配置、没有发送模型请求，无法验证 ready 修复后的真实链路。
- Gateway 为 beta，配置项可能随版本变化；录制当天需重新核对。

## 建议下一步

由主 agent 把 LF-18 口播按本审计收紧：`unconfigured` 落到 web URL/service key、补“ready 不调用 web/provider”。真正的等级升级只能等受保护环境下修复配置、重测 ready 并完成一次真实模型请求。
