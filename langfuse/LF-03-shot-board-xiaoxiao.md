# LF-03《Span、Generation、Tool、Agent》Xiaoxiao 分镜板

用途：给 `zh-CN-XiaoxiaoNeural`、`rate=-5%` 按 20 段原速口播制作画面。口播多长，成片就多长；禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

## 制作规则

- 20 镜使用 20 种不同构图，相邻构图不得重复。
- 每镜画面内只烧一条短字幕，完整口播保留在「口播」列。
- 节点、ID、耗时、类型均为课程示意，不是本次运行的真实数据。
- Tool、Agent 的可用类型与字段以当前 SDK/部署版本为准；支持该语义时才使用。
- 无内网地址、密钥、Authorization 值或真实用户内容。

## 20 镜分镜

| 镜 | 构图 | 时长提示 | 口播 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | 看到一棵调用树，不代表每个节点都记对了。类型混了，后面排查会迷路。 | 树形轮廓从清晰变成错位；中央大字「类型记对了吗？」 | 有调用树，不等于节点都记对了 |
| 02 | `compare-blur` | 6–10s | 检索、工具、模型都只写成“步骤”，你就不知道该查耗时、参数，还是 token。 | 左侧三个真实动作，右侧被压成相同灰块，token 与参数区域模糊 | 都叫“步骤”，排错线索就没了 |
| 03 | `type-grid` | 6–10s | 本集只回答一个问题：Span、Generation、Tool、Agent，分别什么时候用？ | 四个不同色块环绕中央问题，分别标注类型英文 | Span / Generation / Tool / Agent 怎么选 |
| 04 | `span-route` | 6–10s | 检索、解析、路由这类普通处理步骤，用 Span 记录它的开始、结束和输入输出。 | 一条处理路线：retrieve → parse → route，外框标 Span | Span 记录普通处理步骤 |
| 05 | `stopwatch` | 6–10s | Span 帮你看步骤做了什么、花了多久，但一个耗时数字不等于质量好坏。 | 大秒表与输入输出卡，旁边质量标尺留空 | 耗时可以比较，质量仍需单独评估 |
| 06 | `generation-stage` | 6–10s | 模型真正生成内容的那一步，记成 Generation。它和前面的普通处理不是一回事。 | 聚光灯下 prompt → model → output，前序 Span 退到背景 | Generation 专记模型生成 |
| 07 | `metadata-card` | 6–10s | Generation 可以看输入、输出、模型名，以及 token 或成本字段，前提是 SDK 和供应商提供了这些数据。 | 元数据卡：model / input / output / usage；缺失处写 unknown | 有字段才记录，没有就写 unknown |
| 08 | `verdict-split` | 6–10s | 有一条 Generation 记录，不等于答案正确。质量仍然要单独评估。 | 左卡「记录存在」，右卡「答案正确？」，中间醒目不等号 | 记录存在 ≠ 答案正确 |
| 09 | `tool-call` | 6–10s | 当前接入支持 Tool 类型时，实际工具调用可以记成 Tool，重点看工具名、参数、结果和错误。 | 扳手形节点与四格：name / args / result / error；角标「以版本为准」 | Tool 看工具名、参数、结果、错误 |
| 10 | `shield-boundary` | 6–10s | 工具调用有记录，不代表它一定安全。权限、输入边界和失败处理还要单独检查。 | 工具节点外圈盾牌，但权限闸门仍保持待检状态 | 工具已记录 ≠ 工具一定安全 |
| 11 | `agent-orbit` | 6–10s | Agent 用来表达一圈调度工作单元，下面还能挂子步骤。不是只要有模型，就叫 Agent。 | 中央调度环连接三个子步骤；单个模型节点在圈外 | Agent 是调度工作单元，不是模型别名 |
| 12 | `nested-window` | 6–10s | 有了 Agent 节点，也不能直接说全链路可观测完整，还得打开下面的子步骤核对。 | 外层 Agent 窗框，内部子步骤半展开，缺口用虚线 | Agent 节点 ≠ 全链路已经完整 |
| 13 | `scenario-strip` | 6–10s | 举个最小例子：先查资料，再调用一个无副作用工具，最后让模型生成答案。 | 连环三格：固定问题 → 查资料/工具 → 答案；标「固定输入」 | 查资料 → 调工具 → 生成答案 |
| 14 | `typed-flow` | 6–10s | 按真实顺序记录：Trace 包住这次请求，检索是 Span，工具是 Tool，模型回答是 Generation。 | 横向彩色流程，节点下直接标类型，不画虚假耗时 | Trace 里的每一步，都有对应类型 |
| 15 | `tree` | 6–10s | 父子关系要跟着真实调度走。谁发起了谁，就放在对应父节点下面，别为了让树好看去挪。 | Trace → Agent/Span → Generation/Tool 树；错误拖动箭头被打叉 | 父子关系跟着真实调度走 |
| 16 | `checklist` | 6–10s | 验收时核对类型、名称、父节点、输入输出和错误状态；usage 没提供，就如实写 unknown。 | 字段清单逐项高亮：type / name / parentObservationId / input / output / error | 核对类型、父节点、输入输出和错误 |
| 17 | `loop` | 6–10s | UI 出现一棵树还不够。拿到 Trace ID，再按同一个 ID 回读，才能核对它是不是本次运行。 | 请求 → Trace ID → 同一记录回读的闭环；示意 ID 用 `tr_demo_003` | 用同一个 Trace ID 回读核对 |
| 18 | `trend` | 6–10s | 单条树的类型挂对了，也只说明这一次。不能由此推出所有输入都稳定，或模型更好。 | 左侧一棵树，右侧多次运行留白；趋势区标「尚无证据」 | 单条树不能代表整体稳定 |
| 19 | `stamp` | 6–10s | 本集画面是 prototype、L1 示意，不代表当前实例已完成写入、Worker 消费或 UI、API 回读。 | PROTOTYPE / L1 印章，下面列出写入、消费、回读均未证明 | prototype / L1：不是当前实例验收通过 |
| 20 | `cta` | 6–10s | 下一集讲 Prompt 管理：版本和 label 怎么固定，实验才有可比的起点？ | 下一集卡 LF-04，两个 Prompt 版本标签并排，比较按钮保持未启动 | 下一集：Prompt 版本和 label |

## 固定构图顺序

`hook → compare-blur → type-grid → span-route → stopwatch → generation-stage → metadata-card → verdict-split → tool-call → shield-boundary → agent-orbit → nested-window → scenario-strip → typed-flow → tree → checklist → loop → trend → stamp → cta`

## 字幕与旁白

- 声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`，禁止整段变速。
- 首次出现中英并读：Span，步骤；Generation，生成；Tool，工具；Agent，调度工作单元。
- 烧录字幕使用表中短句；SRT、VTT 使用同一时间轴，最后一条与片尾对齐。
- 术语 token、cost、usage 缺失时统一说「未提供 / unknown」，不能补示意数值冒充真实用量。

## 演示与证据边界

1. 录制时锁定 Langfuse 与 SDK 版本，使用脱敏固定输入。
2. 只有在当前 SDK 支持相应语义时记录 Tool、Agent；不得用手工 API 伪造类型或层级。
3. 用同一 Trace ID 核对类型、父节点、输入输出和错误；没有 usage 就保留空值或 unknown。
4. 本文件只定义镜头与概念口径，不证明当前实例写入、消费、回读或模型质量。
5. 单条 Trace、完整树、类型齐全，都不能推出稳定性、模型更好或统计显著。

## 官方来源（检索日期 2026-11-23）

- Observability 数据模型：https://langfuse.com/docs/observability/data-model
- Observability 最佳实践：https://langfuse.com/docs/observability/best-practices
- SDK 文档：https://langfuse.com/docs/sdk
