# LF-19《OTEL 认证门与 Trace ID 回读》Xiaoxiao 分镜板

用途：按 `zh-CN-XiaoxiaoNeural`、`rate=-5%` 为 20 段口播制作画面。口播多长，成片就多长；禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

## 制作规则

- 20 镜使用 20 种不同构图，相邻构图不得重复。
- 每镜画面内只烧一条短字幕，完整口播保留在「口播」列。
- 401/204/405 只能按各自探针范围解释，不是 Trace 写入成功。
- 无内网地址、真实 key/secret、Authorization 值、登录信息、PII 或可复用请求头。

## 20 镜分镜

| 镜 | 构图 | 时长提示 | 口播 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | 请求发到 OTEL 地址，返回 401。这是入口存在、认证门生效，还是 Trace 已写入？只有前两项。 | 401 卡前两格点亮，Trace 写入格保持空白 | 401 说明认证门，不说明 Trace 已写入 |
| 02 | `auth-boundary` | 6–10s | 401 表示凭据缺失或不合法。它连 payload 是否被接收都不能证明，更不是写入成功。 | 认证门停在 payload 之前，后续写入区域不可见 | 401 不能证明 payload 被接收 |
| 03 | `head-method` | 6–10s | HEAD 返回 405，说明这个方法不被接受。不要把方法错误画成服务宕机或写入结果。 | HEAD 405 与 POST 写入通道分开，互不代替 | HEAD 405 不是 Trace 写入结果 |
| 04 | `preflight` | 6–10s | OPTIONS 返回 204，只说明预检有响应。认证、payload 接收和回读都还没被证明。 | 预检卡与认证、接收、回读三道门分开 | OPTIONS 204 只是预检响应 |
| 05 | `legacy-block` | 6–10s | v4 旧 traces、observations 路径出现 events_only 迁移提示，就不要再拿旧路径做回读验收。 | 旧查询路径关闭，当前 UI/API/CLI 路径待核对 | 旧路径的迁移提示不能当回读结果 |
| 06 | `version-pin` | 6–10s | 正式演示先固定 SDK 或 OTEL exporter、server 和运行版本，避免证据来自不同环境。 | 版本卡锁定 SDK/exporter/server/commit，均为占位 | 先固定版本，再开始证据闭环 |
| 07 | `credentials` | 6–10s | 使用受保护的项目凭据发送请求。画面只能出现环境变量占位符，不读取或打印真实值。 | 凭据保险柜连接应用，屏幕只见变量名占位 | 项目凭据只从受保护环境读取 |
| 08 | `request-header` | 6–10s | OTEL 入口、认证方式和 v4 header 按当前官方文档配置，不能靠记忆拼请求。 | 请求模板连接官方文档，header 名可示，值全部隐藏 | 入口和 header 以当前官方文档为准 |
| 09 | `payload-card` | 6–10s | 发送合法、脱敏的最小 payload，保留 payload 摘要或 hash，方便之后核对同一次请求。 | payload 卡包含结构、脱敏标记和 hash 占位 | 最小 payload 要脱敏并留下摘要 |
| 10 | `write-response` | 6–10s | 认证后的写入响应只能记为 write-observed。它说明观察到了响应，还不是完整回读。 | 写入回执卡标 write-observed，回读门尚未打开 | 有写入响应，只到 write-observed |
| 11 | `id-ticket` | 6–10s | 保存本次 Trace ID，无论是返回还是客户端生成，都要能回指同一次运行。 | Trace ID 票根连接请求与运行时间，ID 为示意占位 | Trace ID 是这次运行的回读钥匙 |
| 12 | `flush` | 6–10s | 短生命周期进程退出前执行 flush 或 shutdown，保存日志。没发送完就退出，后面很难补证据。 | 进程退出前 flush 检查点，未完成发送被暂停 | 退出前 flush，保存发送日志 |
| 13 | `worker-consume` | 6–10s | 如果链路包含异步处理，还要观察 Worker 消费。HTTP 接收不等于这条事件已处理。 | HTTP 接收与 Worker 消费两个独立状态卡 | 接收成功 ≠ Worker 已消费 |
| 14 | `query-route` | 6–10s | 回读走当前 v4 支持的 UI、API 或 CLI。具体资源、参数和响应字段以当天 API reference 为准。 | 当前 UI / API / CLI 三条可选回读路径 | 用当前 v4 查询方式，不猜旧接口 |
| 15 | `field-compare` | 6–10s | 核对回读记录的名称、父子关系、时间、输入输出和状态，确认它与请求摘要一致。 | 请求摘要与服务端记录逐字段对照 | 回读要和本次请求逐字段对上 |
| 16 | `time-window` | 6–10s | 写入和回读要保留相同实例、时间窗和采样时间，避免把历史 Trace 当成本次新记录。 | 写入时间与回读时间落在同一证据时间窗 | 同一实例、时间窗，排除历史记录 |
| 17 | `evidence-ladder` | 6–10s | 三级证据别跳级：入口探针是 sampled-pass，写入响应是 write-observed，同 ID 回读才是 e2e-verified。 | 三级阶梯逐级点亮，当前只停在第一层 | 同 ID 回读，才到 e2e-verified |
| 18 | `redaction` | 6–10s | 证据包还要做脱敏和完整性检查：key、内网地址、用户原文不进公开视频，原始文件保留 hash。 | 脱敏门与 SHA-256 清单共同检查证据包 | 证据可复核，也不能泄露敏感信息 |
| 19 | `stamp` | 6–10s | 本集画面是 prototype、L1 示意。当前没有真实项目写入与同 ID 回读，E2E 保持 BLOCKED。 | PROTOTYPE / L1 印章，write/readback 标 BLOCKED | prototype / L1：真实 E2E 仍 BLOCKED |
| 20 | `cta` | 6–10s | 下一集讲 headers、flush 和实时性：为什么请求已经发出，页面上还不一定马上可见？ | LF-20 预告卡：headers / flush / 可见时间三个检查点 | 下一集：发出请求为什么不一定马上可见 |

## 固定构图顺序

`hook → auth-boundary → head-method → preflight → legacy-block → version-pin → credentials → request-header → payload-card → write-response → id-ticket → flush → worker-consume → query-route → field-compare → time-window → evidence-ladder → redaction → stamp → cta`

## 字幕与旁白

- 声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`，禁止整段变速。
- OTEL 读 O-TEL；Trace 首次解释为运行记录，payload 解释为请求数据。
- 烧录字幕使用表中短句；SRT、VTT 使用同一时间轴，最后一条与片尾对齐。
- 不伪造认证成功、2xx、真实 Trace ID、Worker 消费或回读结果。

## 演示与证据边界

1. 固定版本，使用受保护凭据与脱敏最小 payload，保存响应和 Trace ID。
2. flush/shutdown、Worker 消费、当前 v4 UI/API/CLI 回读分别留证。
3. 回读核对名称、父子关系、时间、输入输出和状态，并限制在相同实例与时间窗。
4. 三级证据逐级提升，缺同 ID 回读不能写 e2e-verified。
5. 当前文件只定义概念课画面，不证明当前实例已写入或回读。

## 官方来源（录制当天复核）

- OTEL 集成：https://langfuse.com/integrations/native/opentelemetry
- v4 迁移：https://langfuse.com/integrations/native/opentelemetry/migration-to-v4
- CLI：https://langfuse.com/docs/api-and-data-platform/features/cli
- API reference：https://api.reference.langfuse.com
