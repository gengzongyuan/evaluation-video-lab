# LF-20《OTEL Headers、Flush 与实时性》Xiaoxiao 分镜板

用途：按 `zh-CN-XiaoxiaoNeural`、`rate=-5%` 为 20 段口播制作画面。口播多长，成片就多长；禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

## 制作规则

- 20 镜使用 20 种不同构图，相邻构图不得重复。
- 每镜画面内只烧一条短字幕，完整口播保留在「口播」列。
- 时间戳、响应、Trace ID、重试和可见延迟均为示意或待实测。
- 无内网地址、真实 key/secret、Authorization 值、登录信息、PII 或未脱敏 payload。

## 20 镜分镜

| 镜 | 构图 | 时长提示 | 口播 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | 请求已经发出，页面为什么还看不到 Trace？中间可能隔着认证、批处理、flush 和异步消费。 | 请求已发出，页面记录仍为空，中间四个未知节点 | 发出请求，不等于马上可见 |
| 02 | `four-cards` | 6–10s | 今天只抓四个词：headers、timestamp、flush、readback。每一项都要有证据。 | 四张卡依次翻开：headers / timestamp / flush / readback | headers、时间戳、flush、回读 |
| 03 | `request-headers` | 6–10s | 先按当前文档核对 endpoint、项目认证、Content-Type 和编码。真实 secret 只从受保护环境读取。 | 请求头清单显示字段名与占位符，值全部隐藏 | 请求头按文档核对，密钥不展示 |
| 04 | `v4-header` | 6–10s | v4-ready 直发 OTEL 要带 `x-langfuse-ingestion-version: 4`。只加 header，也不会把旧 payload 自动变正确。 | v4 header 与合法 span 结构同时出现，缺一不可 | v4 header 和合法 span 都要具备 |
| 05 | `delay-doc` | 6–10s | 官方提示，直发 OTEL 缺这个 header 时可能延迟最多十分钟。这是文档口径，不是本地 SLA 实测。 | 十分钟提示卡盖「官方口径」，实测值写 unknown | 文档提示的延迟，不是本地 SLA |
| 06 | `timestamp-pair` | 6–10s | 每个 span 都应同时带 start 和 end 时间戳。它们决定这次调用的时长和排序。 | startTimeUnixNano / endTimeUnixNano 成对出现 | start 和 end 时间戳要同时发送 |
| 07 | `zero-duration` | 6–10s | 如果 start 或 end 缺失、不可解析，官方说明会复制另一端，于是观测可能变成零时长。 | 一端缺失被另一端补齐，时长条收缩成零 | 缺一个时间戳，可能变成零时长 |
| 08 | `ingest-time` | 6–10s | 如果两个时间都缺失，会落到 ingest 时间。你看到的“发生时间”，可能已经不是真实执行时间。 | 原始时间空白，被 ingest 时间替代，差异警示 | 两个时间都缺，会退回 ingest 时间 |
| 09 | `resource-map` | 6–10s | service name、environment 和 trace/span 关系也要核对。它们影响筛选、归因和父子结构。 | 资源属性与调用关系地图，字段名以当前版本为准 | 资源和关联字段影响查询与归因 |
| 10 | `batch-queue` | 6–10s | SDK 或 exporter 常先批量排队。事件已经创建，不代表已经离开当前进程。 | 本地事件队列与网络发送分开，队列仍有待发送项 | 事件已创建，不等于已经发出 |
| 11 | `flush` | 6–10s | 进程退出前执行 flush 或 shutdown，把待发事件送出去，并保存完成或失败日志。 | 退出前 flush 闸门，完成后才允许进程结束 | 退出前 flush，并保存结果日志 |
| 12 | `retry-branch` | 6–10s | 网络抖动会触发重试，也会带来延迟和重复风险。重试次数与最终结果都要记录。 | 首次失败进入 retry 分支，延迟与重复风险同时标记 | 重试要记录次数和最终结果 |
| 13 | `event-log` | 6–10s | 保存创建时间、发送时间、首次响应和 flush 时间。缺了这些点，就很难解释延迟发生在哪。 | 事件日志时间线：create / sent / response / flush | 用时间线定位延迟发生在哪一步 |
| 14 | `readback-loop` | 6–10s | 最后用同一个 Trace ID 回读，确认这条记录已能查询。没有回读，就不说服务端已保存。 | 发送 → Trace ID → 同 ID 回读闭环 | 同 ID 回读，才证明这条记录可查 |
| 15 | `delay-equation` | 6–10s | 可见延迟要定义测量起点，再算到首次成功回读的时间差。起点不同，结果不能直接比较。 | 公式：readback_at − sent_at 或 response_at，先选口径 | 可见延迟必须先定义起点 |
| 16 | `repeat-samples` | 6–10s | 实时性要重复多次，保存 sent、response、readback 和每次 attempt，再谈 p50 或稳定性。 | 多次测量表与 p50 统计卡，数据未测前留空 | 多次测量，才谈 p50 和稳定性 |
| 17 | `screenshot-boundary` | 6–10s | 单次截图只能证明那一刻看到了，不能证明每次都这么快，更不能证明稳定达标。 | 一张可见截图旁，多次运行分布仍为空 | 一次可见 ≠ 实时性稳定 |
| 18 | `redaction` | 6–10s | 公开证据只保留脱敏字段、时间和 hash。真实 key、内网地址、用户原文和完整请求头不能出现。 | 脱敏证据包经过敏感信息检查和 SHA-256 清单 | 留证据，也要遮住密钥和用户数据 |
| 19 | `stamp` | 6–10s | 本集画面是 prototype、L1 示意，真实写入、flush、重试和可见延迟都还没有实测。 | PROTOTYPE / L1 印章，四项实测均标 BLOCKED | prototype / L1：实时性尚未实测 |
| 20 | `cta` | 6–10s | 下一集把整条链落到 Dataset run 和 Score：每条样本、分数与失败，怎样按同一 run 回读？ | LF-21 预告：Dataset → run → Score → readback | 下一集：同一 run 回读样本和 Score |

## 固定构图顺序

`hook → four-cards → request-headers → v4-header → delay-doc → timestamp-pair → zero-duration → ingest-time → resource-map → batch-queue → flush → retry-branch → event-log → readback-loop → delay-equation → repeat-samples → screenshot-boundary → redaction → stamp → cta`

## 字幕与旁白

- 声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`，禁止整段变速。
- OTEL 读 O-TEL；headers 请求头、timestamp 时间戳、flush 刷新发送、readback 回读首次附中英解释。
- 烧录字幕使用表中短句；SRT、VTT 使用同一时间轴，最后一条与片尾对齐。
- 不伪造写入、时间戳、重试次数、真实 Trace ID、可见延迟或 SLA。

## 演示与证据边界

1. 核对 endpoint、认证、v4 header、Content-Type、编码和 exporter 版本。
2. 同时发送 start/end 时间戳，核对 service/environment 和 trace/span 关系。
3. 保存队列、flush/shutdown、响应、重试和同 Trace ID 回读日志。
4. 可见延迟重复多次测量；官方延迟说明不是本地 SLA。
5. 当前文件只定义概念课画面，不证明真实写入或实时性已验证。

## 官方来源（录制当天复核）

- OTEL 集成：https://langfuse.com/integrations/native/opentelemetry
- v4 迁移：https://langfuse.com/integrations/native/opentelemetry/migration-to-v4
