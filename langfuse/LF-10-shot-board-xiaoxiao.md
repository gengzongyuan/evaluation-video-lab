# LF-10《多步骤 Agent 调用树》Xiaoxiao 分镜板

用途：按 `zh-CN-XiaoxiaoNeural`、`rate=-5%` 为 20 段口播制作画面。口播多长，成片就多长；禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

## 制作规则

- 20 镜使用 20 种不同构图，相邻构图不得重复。
- 每镜画面内只烧一条短字幕，完整口播保留在「口播」列。
- Agent、Tool、Generation、节点 ID、耗时和状态都是示意。
- Agent/Tool 的类型与字段以当前 SDK 和部署版本为准，不得手工伪造运行事件。
- 无内网地址、密钥、Authorization 值、PII 或真实业务输入输出。

## 20 镜分镜

| 镜 | 构图 | 时长提示 | 口播 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | 用户只发了一句话，Agent 可能已经规划、查资料、调工具，又改了两次答案。没有调用树，你只看得到最后一句。 | 一句话输入背后连续展开规划、检索、工具、生成多个影子节点 | 最后一句答案，看不见 Agent 的过程 |
| 02 | `agent-loop` | 6–10s | Agent 可以理解成一个会规划并执行多步的工作单元。它不是某一个模型节点的别名。 | 规划 → 执行 → 观察 → 再规划的循环，模型只占其中一格 | Agent 是多步工作单元，不是模型别名 |
| 03 | `trace-container` | 6–10s | 一整次请求先放进 Trace。Agent、检索、工具和模型调用，都要在这棵树里找到对应位置。 | Trace 外框包住多个空位，等待真实步骤进入 | 一次请求，收进同一棵 Trace 树 |
| 04 | `root-map` | 6–10s | 最外层和父子关系要按真实调度画。谁发起了谁，就把谁放到对应父节点下面。 | 根节点到子节点的调度映射，错挂分支被打叉 | 父子关系跟着真实调度走 |
| 05 | `span-card` | 6–10s | 检索或解析是普通处理步骤，可以记成 Span，保留输入输出、起止时间和错误状态。 | Span 卡记录 retrieve / parse 及四个字段 | 检索和解析，先记成普通步骤 |
| 06 | `tool-call` | 6–10s | 当前 SDK 支持 Tool 类型时，外部工具调用记成 Tool，重点看工具名、参数、结果和错误。 | 工具卡连接外部能力，name / args / result / error 四格 | Tool 记录一次真实外部能力调用 |
| 07 | `generation-stage` | 6–10s | 模型真正生成内容的那一步记成 Generation，再核对模型名、输入输出和实际返回的 usage。 | 聚光灯下 prompt → model → output，usage 缺失写 unknown | Generation 单独记录模型调用 |
| 08 | `iteration` | 6–10s | Agent 可能拿工具结果再调用一次模型。第二次生成要保留自己的节点，不要覆盖上一次。 | 工具结果回到模型形成第二轮，两次 Generation 独立编号 | 每一轮模型调用，都保留自己的节点 |
| 09 | `tree` | 6–10s | 把这些节点展开，才是可解释的调用树：一次请求、一个调度单元，以及下面真实的步骤。 | 完整示意树逐层展开：Trace → Agent → Span/Tool/Generation | 把调度、工具和模型展开成一棵树 |
| 10 | `field-card` | 6–10s | 每个节点至少核对类型、名称、父节点、输入输出和状态，具体字段名按当前版本确认。 | 字段卡：type / name / parentObservationId / input / output / status | 类型、名称、父节点、输入输出都要核对 |
| 11 | `error-node` | 6–10s | 某个工具失败时，失败应该落在真实节点上。不要只把整棵 Trace 标红，让你仍找不到出错点。 | 单个 Tool 节点变红，父 Trace 保持可展开 | 错误要落在真实的失败节点上 |
| 12 | `redaction` | 6–10s | 树的输入输出可能含敏感数据。录制和上传前先脱敏，错误堆栈也不能直接公开。 | 输入输出和错误栈经过遮罩，公开画面只留结构 | 输入输出和错误堆栈都要脱敏 |
| 13 | `waterfall` | 6–10s | 把树切换成时间瀑布，才能看出检索、工具和模型各花了多久。示意条不能当实测。 | 同棵树映射到时间瀑布，耗时数值留空 | 树看结构，瀑布看时间花在哪里 |
| 14 | `orphan` | 6–10s | 检查孤立节点。它看起来有记录，却没有正确父级，往往意味着上下文没有串起来。 | 一个节点脱离树外，parentObservationId 为空 | 孤立节点说明调用关系可能断了 |
| 15 | `duplicate` | 6–10s | 还要检查重复节点。一次工具调用被记两遍，会同时影响耗时、费用和失败统计。 | 同一调用出现重复副本，第二份被红框标记 | 重复记录会污染耗时和统计 |
| 16 | `missing-branch` | 6–10s | 树里没看到的分支，不一定没发生。采样、过滤或漏接都可能让一部分过程消失。 | 实线已知分支与虚线未知分支并存，缺口明确可见 | 树里没看到，不等于过程没发生 |
| 17 | `readback-loop` | 6–10s | 真正验收时，用同一个 Trace ID 回读整棵树，核对类型、父子关系、状态和时间。 | 请求 → Trace ID → 树回读 → 字段核对闭环 | 同一个 Trace ID 回读整棵树 |
| 18 | `decision-shield` | 6–10s | 一棵完整的树，也不证明 Agent 决策正确或工具安全。质量和权限仍需单独评估。 | 完整树旁的质量与权限两扇独立门尚未通过 | 树完整 ≠ 决策正确或工具安全 |
| 19 | `stamp` | 6–10s | 本集画面是 prototype、L1 示意，不代表当前实例已写入或回读这条 Agent 调用树。 | PROTOTYPE / L1 印章，写入与回读标未证明 | prototype / L1：不是 Agent 树已跑通 |
| 20 | `cta` | 6–10s | 下一集讲实验比较：同一 Dataset 上，怎样公平比较两个 Prompt 或模型？ | LF-11 预告卡：同一 Dataset 分流到两个候选版本 | 下一集：同组样本比较 Prompt 或模型 |

## 固定构图顺序

`hook → agent-loop → trace-container → root-map → span-card → tool-call → generation-stage → iteration → tree → field-card → error-node → redaction → waterfall → orphan → duplicate → missing-branch → readback-loop → decision-shield → stamp → cta`

## 字幕与旁白

- 声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`，禁止整段变速。
- 首次出现保留英文并给中文解释：Trace 运行记录、Span 普通步骤、Tool 工具调用、Generation 模型生成。
- 烧录字幕使用表中短句；SRT、VTT 使用同一时间轴，最后一条与片尾对齐。
- 不编造真实节点、延迟、用量、错误率或 Agent 质量结论。

## 演示与证据边界

1. 使用固定脱敏输入和受保护环境，按当前 SDK 创建并结束父子 Observation。
2. 同一轮回读类型、名称、父节点、状态、错误和时间；检查孤立、重复和缺失分支。
3. Tool/Generation 输入输出与错误堆栈必须脱敏，usage 缺失写 unknown。
4. 树完整不能证明任务质量、决策正确、工具安全或所有分支完整。
5. 当前文件只定义概念课画面，不证明当前实例已写入或回读。

## 官方来源（录制当天复核）

- Observability：https://langfuse.com/docs/observability
- 数据模型：https://langfuse.com/docs/observability/data-model
