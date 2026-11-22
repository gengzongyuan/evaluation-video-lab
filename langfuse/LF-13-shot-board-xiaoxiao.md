# LF-13《自托管架构与健康检查》Xiaoxiao 分镜板

用途：按 `zh-CN-XiaoxiaoNeural`、`rate=-5%` 为 20 段口播制作画面。口播多长，成片就多长；禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

## 制作规则

- 20 镜使用 20 种不同构图，相邻构图不得重复。
- 每镜画面内只烧一条短字幕，完整口播保留在「口播」列。
- 拓扑、端点响应、组件状态、版本和恢复结果均为示意或待验证。
- health/readiness 只是时间点信号，不能替代写入、消费、持久化、回读和恢复证据。
- 无内网地址、密钥、Authorization 值、登录信息、PII 或可复用请求头。

## 20 镜分镜

| 镜 | 构图 | 时长提示 | 口播 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | 浏览器能打开，就代表 Trace 能写入、Worker 能消费、对象能存储吗？当然不能。 | 已打开网页后方的写入、Worker、存储三盏灯仍是未知 | 页面能打开，不等于全链路正常 |
| 02 | `topology` | 6–10s | 自托管 Langfuse 不只是一个网页。Web、Worker、数据库、Redis 和对象存储各自承担不同职责。 | 五组件拓扑，连线为逻辑职责而非已验证流量 | 自托管是一组组件，不只是一个网页 |
| 03 | `web-card` | 6–10s | Web 和 API 负责界面与请求入口。它能响应，只说明这一条入口当时可访问。 | Web/API 入口卡，响应与后端写入分开 | Web 响应 ≠ 后端链路已验证 |
| 04 | `worker-queue` | 6–10s | Worker 负责异步任务。API 收到请求以后，后台任务是否真正消费，要单独观察。 | API 请求进入队列，Worker 消费状态单独待核对 | API 收到 ≠ Worker 已消费 |
| 05 | `database-split` | 6–10s | PostgreSQL 和 ClickHouse 承担不同持久化与分析职责，具体分工以当前部署文档为准。 | 双数据库卡：关系数据 / 分析数据，字段不写死 | 数据库职责要按当前部署核对 |
| 06 | `redis-lanes` | 6–10s | Redis 常承担队列或缓存等协调职责。队列能接收，也不等于任务已经处理完成。 | Redis 队列与缓存双泳道，消费完成标记留空 | 入队不等于任务完成 |
| 07 | `object-storage` | 6–10s | MinIO 或 S3 负责对象类数据。要验证的不只是服务在线，还包括对象实际写入和读取。 | 对象存储桶卡，写入与读取是两个独立检查点 | 对象存储要验证实际写入和读取 |
| 08 | `health-pulse` | 6–10s | `/api/public/health` 可以作为服务是否响应的快速信号，但 200 只代表当时的健康检查。 | health 脉冲卡带时间点，后端全链路保持未知 | health 200 只是当时的响应信号 |
| 09 | `readiness-gate` | 6–10s | readiness 用来检查服务是否准备好接流量。它也不能替代真实请求、异步消费或对象读写。 | readiness 门只打开接流量入口，后续三道门仍关闭 | ready ≠ 写入、消费、回读都通过 |
| 10 | `worker-health` | 6–10s | Worker 要单独看健康与消费证据。Web health 正常，不能代替 Worker 的状态。 | Web 与 Worker 两张独立健康卡，不共享通过状态 | Web 健康，不代表 Worker 健康 |
| 11 | `e2e-chain` | 6–10s | 最小全链路验证是：发起受保护写入，观察 Worker 消费，检查持久化，再用同一 ID 回读。 | 写入 → 消费 → 持久化 → 同 ID 回读链条 | 写入、消费、持久化、回读要连起来 |
| 12 | `object-readback` | 6–10s | 涉及对象时，还要用对象标识回读同一份内容，核对大小、权限和脱敏结果。 | 对象 ID 回读卡，大小与权限栏待实际值 | 对象也要用同一标识回读 |
| 13 | `version-matrix` | 6–10s | 录制时固定 server、SDK、runtime 和部署版本。只说“最新版”，之后很难复现。 | 版本矩阵逐项锁定，日期与 commit 一并记录 | 固定 server、SDK、runtime 和部署版本 |
| 14 | `digest-card` | 6–10s | 镜像要记录 digest。`latest` 只是标签，不能证明下次拉到的还是同一份镜像。 | latest 标签旁显示 digest 占位，二者明确区分 | 用镜像 digest 固定实际部署内容 |
| 15 | `restart-timeline` | 6–10s | 重启恢复要记录依赖顺序、失败日志和恢复时间。进程重新启动，不等于数据链路已经恢复。 | 重启时间线：停止 → 依赖 → 启动 → 回读，最后一步待验证 | 重启成功 ≠ 数据链路已恢复 |
| 16 | `backup-map` | 6–10s | 备份要覆盖真正持久化的数据，记录清单、权限和加密。只写“已配置”，不能证明备份可用。 | 数据库与对象存储进入备份清单，权限和加密单独检查 | 备份配置 ≠ 备份可恢复 |
| 17 | `restore-drill` | 6–10s | 在隔离环境做恢复演练，记录实际结果和观察到的 RPO、RTO。没演练，就不要说达标。 | 隔离恢复区与生产区分开，RPO/RTO 未实测写 unknown | 恢复能力要靠隔离演练证明 |
| 18 | `security-boundary` | 6–10s | 公开视频不得暴露内网地址、密钥和登录信息。健康端点通过，也不能证明公网与权限安全。 | 地址、登录、密钥全部遮盖，TLS/权限验收项留白 | health 通过 ≠ 公网和权限安全 |
| 19 | `stamp` | 6–10s | 本集画面是 prototype、L1 示意，不代表当前部署已完成全链路、重启或备份恢复验收。 | PROTOTYPE / L1 印章，全链路、重启、恢复均标未证明 | prototype / L1：不是自托管已验收 |
| 20 | `cta` | 6–10s | 下一集讲版本锁定：SDK 和 server 的兼容关系，怎样在升级前核对并留下证据？ | LF-14 预告卡：SDK 与 server 版本配对，升级门待验证 | 下一集：SDK 与 server 版本锁定 |

## 固定构图顺序

`hook → topology → web-card → worker-queue → database-split → redis-lanes → object-storage → health-pulse → readiness-gate → worker-health → e2e-chain → object-readback → version-matrix → digest-card → restart-timeline → backup-map → restore-drill → security-boundary → stamp → cta`

## 字幕与旁白

- 声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`，禁止整段变速。
- 首次出现保留英文并给中文解释：Worker 后台任务处理器、health 健康检查、readiness 就绪检查、digest 镜像摘要。
- 烧录字幕使用表中短句；SRT、VTT 使用同一时间轴，最后一条与片尾对齐。
- 不编造组件健康、真实 ID、版本、恢复时间、RPO/RTO 或安全结论。

## 演示与证据边界

1. 保存环境、时间、server/SDK/runtime 版本、部署 commit 或镜像 digest。
2. 分开保存 Web、Worker、数据库、队列、对象存储的健康与依赖证据。
3. 同轮完成写入、消费、持久化、回读；涉及对象时回读同一对象。
4. 重启与备份恢复必须隔离演练并保留结果，未执行保持 `BLOCKED`。
5. 当前文件只定义概念课画面，不证明当前部署全链路或生产安全已验证。

## 官方来源（录制当天复核）

- 自托管入口：https://langfuse.com/self-hosting
- 部署文档：https://langfuse.com/docs/deployment
