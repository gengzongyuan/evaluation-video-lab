# LF-17《Health 与 Readiness》Xiaoxiao 分镜板

用途：按 `zh-CN-XiaoxiaoNeural`、`rate=-5%` 为 20 段口播制作画面。口播多长，成片就多长；禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

## 制作规则

- 20 镜使用 20 种不同构图，相邻构图不得重复。
- 每镜画面内只烧一条短字幕，完整口播保留在「口播」列。
- 状态码和组件状态若引用历史采样，必须标采样时间；不代表此刻状态。
- 无内网地址、端口拓扑、密钥、Authorization 值、登录信息或 PII。

## 20 镜分镜

| 镜 | 构图 | 时长提示 | 口播 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | 同一个部署，health 返回 200，ready 却返回 503。矛盾吗？不矛盾，它们检查的不是同一层。 | health 200 与 ready 503 并列，两个检查范围不同 | health 200 和 ready 503 可以同时存在 |
| 02 | `health-card` | 6–10s | Web 的 health 先回答 API 是否在运行。默认情况下，它不检查数据库连通性。 | `/api/public/health` 卡只覆盖 API 进程，数据库在框外 | Web health 默认不检查数据库 |
| 03 | `db-flag` | 6–10s | 要把数据库纳入健康检查，要加 `failIfDatabaseUnavailable=true`。参数名按当前文档核对。 | health 请求增加数据库参数，数据库进入检查范围 | 加数据库参数，才多检查一层依赖 |
| 04 | `ready-gate` | 6–10s | readiness 回答服务是否可以接收流量。收到关闭信号时会拒绝接流量，但这不是业务验收。 | ready 闸门允许/拒绝流量，业务验证仍在门后 | ready 检查接流量，不是业务验收 |
| 05 | `compare-signals` | 6–10s | health 和 ready 可以一绿一红，因为进程活着，不等于服务此刻应该接新流量。 | 进程存活与流量准入双轴，四种组合不被混为一谈 | 进程活着，不等于应该接新流量 |
| 06 | `web-scope` | 6–10s | Web ready 通过，也只覆盖 Web 自身。Worker、数据库、对象存储和真实请求还要分别核对。 | Web 通过卡之外，四个依赖区仍待检查 | Web ready 不能代替整个系统 |
| 07 | `worker-health` | 6–10s | Worker 有独立 `/api/health`，检查 Worker 服务与数据库连接。Web 的结果不能拿来代填。 | Worker 独立健康卡，不从 Web 复制状态 | Worker 健康必须单独检查 |
| 08 | `queue-boundary` | 6–10s | Worker health 通过，也不代表队列没有积压，或你刚才那条 Trace 已处理。 | Worker 健康卡旁的队列积压与单条任务仍未知 | Worker 健康 ≠ 队列无积压 |
| 09 | `stuck-probes` | 6–10s | 当前文档还提供事件传播和队列消费的 stuck 探针。它们能补盲区，但仍不是端到端回读。 | 两类 stuck 探针连接 Worker，端到端回读独立保留 | stuck 探针也不能代替 Trace 回读 |
| 10 | `minio-liveness` | 6–10s | MinIO liveness 通过，只说明对象存储进程存活。对象能否写入、读取和恢复，要另测。 | 对象存储存活卡与读写、恢复三栏分开 | 存储进程活着，不等于对象可读写 |
| 11 | `gateway-split` | 6–10s | Gateway 也一样：health 通过不代表配置就绪。历史采样里 ready `unconfigured` 就是反例。 | Gateway health 与 ready 分屏，后者标历史采样风险 | Gateway health ≠ Gateway ready |
| 12 | `timestamp` | 6–10s | 所有端点结果都要带采样时间。昨天是 200，不能剪成现在一定还是 200。 | 端点快照卡带日期与“时间点采样”印章 | 端点状态只代表采样那一刻 |
| 13 | `layer-map` | 6–10s | 正确的排查顺序是：进程响应、依赖就绪、Worker 状态、真实业务链路。缺一层就保留缺口。 | 四层阶梯逐层上升，缺层时最高层不通过 | 按层检查，不用一个 200 代替全部 |
| 14 | `write-step` | 6–10s | 业务验收先用受保护凭据发起一条真实 Trace 写入，保存响应和 Trace ID。 | 真实写入步骤卡，凭据隐藏，ID 用脱敏占位 | 先留下真实写入响应和 Trace ID |
| 15 | `consume-step` | 6–10s | 再观察 Worker 是否消费这条事件。API 接收成功，不能替代消费证据。 | 写入事件进入 Worker，消费状态独立记录 | API 接收 ≠ Worker 已消费这条事件 |
| 16 | `readback-loop` | 6–10s | 最后用同一个 Trace ID 回读，核对输入、输出、父子关系和时间，确认是本次运行。 | 写入 → 消费 → 同 ID 回读闭环 | 同 ID 回读，才闭合这条运行证据 |
| 17 | `recovery-boundary` | 6–10s | health 和 ready 也不能证明重启恢复、备份恢复或生产安全。那些需要单独演练和审计。 | 健康卡之外的重启、备份、安全三项均标未验证 | 健康检查不覆盖恢复和安全演练 |
| 18 | `redaction` | 6–10s | 公开视频只保留必要状态和时间，遮住内网地址、端口、登录信息和可定位拓扑。 | 地址、端口、登录与拓扑全部脱敏 | 展示状态，不暴露地址和拓扑细节 |
| 19 | `stamp` | 6–10s | 本集画面是 prototype、L1 示意，不代表当前实例已写入、消费或回读新 Trace。 | PROTOTYPE / L1 印章，写入、消费、回读均标未证明 | prototype / L1：不是 Trace 链路已验收 |
| 20 | `cta` | 6–10s | 下一集专看 Gateway：为什么 ready 变成 200 以后，真实模型请求仍然要单独测？ | LF-18 预告卡：ready → 真实模型请求，两者不合并 | 下一集：Gateway ready 之后还要测什么 |

## 固定构图顺序

`hook → health-card → db-flag → ready-gate → compare-signals → web-scope → worker-health → queue-boundary → stuck-probes → minio-liveness → gateway-split → timestamp → layer-map → write-step → consume-step → readback-loop → recovery-boundary → redaction → stamp → cta`

## 字幕与旁白

- 声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`，禁止整段变速。
- 首次出现保留英文并给中文解释：health 健康检查、readiness 就绪检查、Worker 后台任务处理器、Trace 运行记录。
- 烧录字幕使用表中短句；SRT、VTT 使用同一时间轴，最后一条与片尾对齐。
- 不伪造端点通过、真实 Trace ID、Worker 消费、回读或恢复结果。

## 演示与证据边界

1. 按官方端点分别采样 Web、Worker、Gateway、MinIO，并记录时间和参数。
2. Web health 默认不查数据库；Worker 与队列状态独立检查。
3. 业务验收保存真实写入、Worker 消费和同 Trace ID 回读。
4. 端点采样不能证明重启、备份、权限或生产安全；缺失保持 `BLOCKED`。
5. 当前文件只定义概念课画面，不证明当前实例业务链路已通过。

## 官方来源（录制当天复核）

- Health / readiness 端点：https://langfuse.com/self-hosting/configuration/health-readiness-endpoints
- Docker Compose：https://langfuse.com/self-hosting/deployment/docker-compose
