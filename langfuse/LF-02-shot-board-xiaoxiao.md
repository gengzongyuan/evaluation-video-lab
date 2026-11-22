# LF-02《Trace 是什么》Xiaoxiao 分镜板

用途：按 [LF-02-voice-script-xiaoxiao.md](LF-02-voice-script-xiaoxiao.md) 的 20 段原速口播做画面。声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`。口播多长成片就多长，禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

规则：

- 20 个镜头使用 20 种不同构图，相邻镜头构图不得相同。
- 每镜底部烧录一句字幕，不要把整段口播铺满屏幕。
- 画面是课程示意，不是当前实例 Trace 写入或回读证据。
- 不得出现内网地址、项目密钥、Authorization 值、真实用户内容。

## 分镜表

| 镜 | 构图 | 时长提示 | 口播要点 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | 用户一句话，后台可能已跑完检索、工具、模型 | 超大标题「错在哪一步？」；一句话输入拆成三个未点亮节点 | 只看最终答案，看不出哪一步出错 |
| 02 | `compare-log` | 6–10s | 普通日志只留失败或最终回复 | 左侧终端只剩一行 `request failed`；右侧过程区全黑 | 普通日志常常只留下一句失败 |
| 03 | `record-card` | 6–10s | 整次请求记成一条 Trace | 就诊记录卡：请求开始 → 请求结束；标题 Trace = 追踪 | Trace：一次完整请求，像就诊记录 |
| 04 | `nested-container` | 6–10s | Trace 是容器，不是某一个模型答案 | 外框写 Trace，里面淡化多个空节点，答案只占一角 | Trace 是容器，不是某一个模型答案 |
| 05 | `split` | 6–10s | 日志是散落的行，Trace 是调用树 | 左：12:01 retrieve / 12:01 tool / 12:02 answer；右：树形 Trace | 日志是散落的行，Trace 是一棵调用树 |
| 06 | `tree` | 6–10s | Observation 是可观察动作，可挂子节点 | 展开树：Trace → Observation → 子节点；旁注「观察节点」 | Observation：树里每一个可观察动作 |
| 07 | `span-card` | 6–10s | 检索或工具调用通常记成 Span | 三张步骤卡：retrieve / parse / tool，标注 Span = 步骤 | Span 用来记检索、解析、工具这些步骤 |
| 08 | `generation` | 6–10s | 模型生成记成 Generation | 竖向三步：prompt → model → output，标注输入/输出/模型 | Generation：模型真正生成文字的那一步 |
| 09 | `bars` | 6–10s | 从总耗时往下钻 | 三条时长条：retrieve 短、tool 报错红、generation 最长 | 是检索慢、模型慢，还是工具报错 |
| 10 | `pipeline` | 6–10s | 最小链路 | 五个色块加箭头：提问 → 检索 → 工具 → 模型 → 答案 | 提问 → 检索 → 工具 → 模型 → 答案 |
| 11 | `id-card` | 6–10s | 整次请求共用一条 Trace ID | 脱敏 ID 卡：`tr_demo_001`（示意）；旁边划掉「只翻终端」 | 排错先拿 Trace ID，不要只翻滚动日志 |
| 12 | `three-questions` | 6–10s | 失败时先问三句 | 失败节点变红，旁边三问：节点 / 输入 / 耗时与输出 | 失败节点是哪一个？输入和输出有没有异常？ |
| 13 | `inspect` | 6–10s | 核对输入、输出、时间、状态 | 检查清单四项打勾框，页面缩略图只作背景且标「示意」 | 要核对输入、输出、时间和状态 |
| 14 | `warning` | 6–10s | 页面打开 ≠ 写入成功 | 浏览器窗口「已打开」上打大红叉，旁注未证明写入 | 页面能打开，不代表 Trace 已经写入 |
| 15 | `not-equal` | 6–10s | health 200 只是当时健康检查 | 左卡 health 200，中间 ≠，右卡 new Trace | health 200 ≠ 新 Trace |
| 16 | `blocked` | 6–10s | 不能证明写入，也不能证明同 ID 回读 | 三张未证明条：写入 / 回读 / 同一 ID | 不能证明新 Trace 已写入或可回读 |
| 17 | `loop` | 6–10s | 发出请求 → Trace ID → 同一条回读 | 三步闭环，箭头回到同一张记录卡 | 请求 → Trace ID → 同一条回读 |
| 18 | `trend` | 6–10s | 单条 Trace 不能代表整体稳定 | 左：一条运行；右：多次趋势虚线并盖「未证明」 | 单条 Trace 不能代表整体稳不稳定 |
| 19 | `stamp` | 6–10s | 本集只讲差别，画面是 L1 示意 | 大红章 PROTOTYPE / L1；注明不是写入或回读成功 | prototype / L1：示意，不是写入或回读成功 |
| 20 | `cta` | 6–10s | 下一集拆 Span 和 Generation | 下一集卡：LF-03；问题：为什么模型调用要单独记？ | 下一集：为什么模型调用要单独记？ |

## 构图不得相邻重复

顺序固定为：hook → compare-log → record-card → nested-container → split → tree → span-card → generation → bars → pipeline → id-card → three-questions → inspect → warning → not-equal → blocked → loop → trend → stamp → cta。

## 字幕与旁白

- 烧录字幕用上表短句；完整口播见口播稿，不要把整段一次性铺到画面上。
- 首次出现中英并读：Trace 追踪、Observation 观察节点、Span 步骤、Generation 生成。
- SRT 与 VTT 必须同一时间轴，结束点对齐成片，不得把字幕拉长去填 180 秒。

## 证据边界

- 本分镜只服务概念课和制作流程，证明不了当前实例已写入 Trace、Worker 已消费、或 UI/API 回读成功。
- `tr_demo_001`、时长条、失败节点变红都是示意，禁止口播成真实 run。
- health 200 只能说成时间点采样，不能说成新 Trace。
- 单条 Trace 不能说成稳定性、模型更好或统计显著。

## 官方来源（检索日期 2026-11-22）

- Tracing 概览：https://langfuse.com/docs/observability/overview
- 数据模型：https://langfuse.com/docs/observability/data-model
- SDK 入口：https://langfuse.com/docs/sdk
