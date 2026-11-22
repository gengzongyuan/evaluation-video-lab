# LF-16《Langfuse v4 与 OTEL 迁移》Xiaoxiao 分镜板

用途：按 `zh-CN-XiaoxiaoNeural`、`rate=-5%` 为 20 段口播制作画面。口播多长，成片就多长；禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

## 制作规则

- 20 镜使用 20 种不同构图，相邻构图不得重复。
- 每镜画面内只烧一条短字幕，完整口播保留在「口播」列。
- 响应码、Trace ID、payload 和运行状态均为示意或历史探针边界，不能当新写入证据。
- 具体 SDK、OTEL 参数、headers 和查询方式以录制当天官方文档为准。
- 无内网地址、真实密钥、Authorization 值、登录信息、PII 或可复用请求头。

## 20 镜分镜

| 镜 | 构图 | 时长提示 | 口播 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | 旧接口返回 404，就一定是服务挂了吗？不一定。先看错误里有没有 v4 的迁移提示。 | 404 卡中央放大 `events_only` 迁移信号，而非“服务宕机” | 旧接口 404，也可能是迁移信号 |
| 02 | `legacy-paths` | 6–10s | 先分清旧路径：迁移指南讲的 `/api/public/ingestion`，和现场探针访问的 traces、observations，不是同一个接口。 | 两条旧路径分栏，禁止合并成“旧 API 都一样” | 不同旧接口，不要混成同一个路径 |
| 03 | `migration-signal` | 6–10s | `events_only` 告诉你旧写入方式已经需要迁移，不代表新 Trace 已写入，也不代表服务全部不可用。 | 迁移路标指向新链路，旧路径只保留提示含义 | events_only 是迁移提示，不是写入成功 |
| 04 | `sdk-road` | 6–10s | 官方迁移方向是 Python SDK v5、JS/TS SDK v6。录制当天仍要核对版本和升级指南。 | 两条 SDK 升级道路，附文档核对日期，不显示项目已升级 | 优先按当前 SDK 与升级指南迁移 |
| 05 | `otel-choice` | 6–10s | 自定义集成或其他语言可以使用 OpenTelemetry。迁移不是只换一个 URL。 | SDK 与 OTEL 两条选择路径，后者包含完整数据与上下文 | 选 OTEL，也不是只改一个 URL |
| 06 | `endpoint-card` | 6–10s | OTLP over HTTP 的 traces 入口是 `/api/public/otel/v1/traces`。入口存在不等于数据落库。 | OTEL endpoint 卡与落库状态分开，后者未知 | OTEL 入口可达 ≠ 数据已落库 |
| 07 | `auth-gate` | 6–10s | 项目认证使用 Basic Auth，真实凭据只从受保护环境读取。画面里只显示字段名，不显示值。 | 认证门只显示占位符，密钥区域完全遮盖 | 项目凭据只从受保护环境读取 |
| 08 | `header-card` | 6–10s | v4-ready 请求还要按官方文档带 `x-langfuse-ingestion-version: 4`，不要凭记忆猜 header。 | 指定 header 与官方文档页绑定，字段来源可回指 | v4 header 要按官方文档核对 |
| 09 | `span-schema` | 6–10s | 每个操作需要完整 span，包括合法 trace ID、span ID、时间和父级上下文，不是把旧 JSON 换个地址。 | span 结构卡：IDs / time / parent context，均为示意 | 完整 span 和上下文，不是旧 JSON 换地址 |
| 10 | `real-execution` | 6–10s | 演示必须来自真实执行和导出，不要手工伪造事件或父子关系来让画面好看。 | 应用执行 → exporter → OTEL，手工伪事件路径被打叉 | 迁移证据来自真实执行，不是手工造数 |
| 11 | `request-checklist` | 6–10s | 发送前核对 Content-Type、编码、最小脱敏 payload 和 exporter 版本，保留请求摘要。 | 请求检查清单逐项点亮，payload 不含真实内容 | 编码、payload、exporter 版本都要留证 |
| 12 | `preflight` | 6–10s | OPTIONS 返回 204，只能说明预检响应被观察到。它不证明认证通过、payload 接收或回读成功。 | 204 预检卡与认证、接收、回读三道门分离 | OPTIONS 204 ≠ Trace 写入成功 |
| 13 | `unauthorized` | 6–10s | 空请求返回 401，只说明入口要求有效认证，或凭据缺失、不合法。不能把它写成上报成功。 | 401 认证门关闭，Trace 写入区完全为空 | 401 是认证边界，不是上报成功 |
| 14 | `health-boundary` | 6–10s | health 200 也只是时间点健康信号，不能代替 OTEL 写入、Worker 消费或同 ID 回读。 | health 卡与 OTEL 全链路分开，全链路标未证明 | health 200 ≠ OTEL 链路通过 |
| 15 | `sdk-benefits` | 6–10s | 官方建议 Python、JS/TS 优先用 SDK，让它处理属性、上下文、过滤和导出，减少手工拼协议的错误。 | SDK 封装属性和上下文，手工拼协议退到备选路径 | 能用官方 SDK，就少手工拼协议 |
| 16 | `flush` | 6–10s | 短生命周期进程要在退出前 flush 或 shutdown，并保存日志。进程结束不代表数据已经发送完。 | 进程退出前的 flush/shutdown 检查点，日志区域保留 | 退出前 flush，进程结束不等于已发送 |
| 17 | `readback-loop` | 6–10s | 真正验收要拿到 Trace ID，再按同一个 ID 回读，核对名称、父子关系、时间和输入输出。 | 写入 → Trace ID → 当前 UI/API → 同一条记录闭环 | 同一 Trace ID 回读，才算链路有证据 |
| 18 | `delay-warning` | 6–10s | 官方文档提示，直发 OTEL 缺少 v4 header 时可能出现延迟。这是文档口径，不是本地实时性实测。 | 延迟警告卡标官方口径，实测值保持 unknown | 文档提示的延迟，不是本地 SLA 实测 |
| 19 | `stamp` | 6–10s | 本集画面是 prototype、L1 示意，不代表当前实例已完成 OTEL 写入、Worker 消费或回读。 | PROTOTYPE / L1 印章，写入、消费、回读均标未证明 | prototype / L1：不是 OTEL 迁移已验收 |
| 20 | `cta` | 6–10s | 下一集继续拆 health 和 readiness：两个端点都通过，为什么仍然不能代替真实 Trace 回读？ | LF-17 预告卡：health / readiness / Trace 回读三道独立门 | 下一集：health、ready 与真实回读的区别 |

## 固定构图顺序

`hook → legacy-paths → migration-signal → sdk-road → otel-choice → endpoint-card → auth-gate → header-card → span-schema → real-execution → request-checklist → preflight → unauthorized → health-boundary → sdk-benefits → flush → readback-loop → delay-warning → stamp → cta`

## 字幕与旁白

- 声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`，禁止整段变速。
- OTEL 口播读 O-TEL；Trace 首次解释为运行记录，SDK 首次解释为开发工具包。
- 烧录字幕使用表中短句；SRT、VTT 使用同一时间轴，最后一条与片尾对齐。
- 不伪造 2xx、真实 Trace ID、迁移完成、Worker 消费、回读或实时性结果。

## 演示与证据边界

1. 区分旧 ingestion 与 traces/observations 路径，按当前迁移指南操作。
2. 锁定 SDK/exporter/server 版本，使用受保护凭据、v4 header 和脱敏真实 span。
3. 保存响应、Trace ID、flush/shutdown 与同 ID 回读；401/204/health 都不是成功证据。
4. 缺项目权限或回读证据保持 `BLOCKED`，无凭据参考代码不能说成已运行。
5. 当前文件只定义概念课画面，不证明当前实例迁移或写入已成功。

## 官方来源（录制当天复核）

- v4 迁移：https://langfuse.com/integrations/native/opentelemetry/migration-to-v4
- OTEL 集成：https://langfuse.com/integrations/native/opentelemetry
- SDK 概览：https://langfuse.com/docs/observability/sdk/overview
- SDK 升级路径：https://langfuse.com/docs/observability/sdk/upgrade-path
