# LF-06《Evaluation、Score 与失败样本》Xiaoxiao 分镜板

用途：按 `zh-CN-XiaoxiaoNeural`、`rate=-5%` 为 20 段口播制作画面。口播多长，成片就多长；禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

## 制作规则

- 20 镜使用 20 种不同构图，相邻构图不得重复。
- 每镜画面内只烧一条短字幕，完整口播保留在「口播」列。
- Score、分数、样本量、失败类型和关联 ID 都是示意，不是真实实验结果。
- 评分字段与 SDK 参数以录制当天官方文档和部署版本为准。
- 无内网地址、密钥、Authorization 值、PII 或真实业务输入输出。

## 20 镜分镜

| 镜 | 构图 | 时长提示 | 口播 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | 总分九十，就能上线吗？先别急着点头，一个平均数可能把关键失败藏起来。 | 巨大「90 分」占屏，角落红色失败样本被遮挡 | 总分 90，也不能直接决定上线 |
| 02 | `average-mask` | 6–10s | 多数样本表现好，不代表所有关键场景都安全。平均分要和失败样本一起看。 | 平滑平均分条下露出一条红色严重失败，旁边标「示意」 | 平均分会掩盖关键失败 |
| 03 | `score-card` | 6–10s | Score 是绑定到运行证据上的评价结果。它不是脱离样本、独立存在的真理。 | Score 卡连接 Trace / run / 原始输出三条证据线 | Score 要绑定具体运行证据 |
| 04 | `evaluation-cycle` | 6–10s | Evaluation 是定义问题、执行评分、检查结果和复核失败的完整过程，不只是写一个数字。 | 环形四步：定义 → 评分 → 检查 → 复核 | Evaluation 不只是得到一个分数 |
| 05 | `rubric` | 6–10s | 先写清你到底评什么，例如是否包含必需字段。问题不清楚，分数再精确也没用。 | 评分问题卡，例子只写「是否包含必需字段」 | 先定义评分问题，再谈分数 |
| 06 | `scale` | 6–10s | 再确定范围、单位、空值和失败判定。缺失值不能悄悄当成零分或满分。 | 刻度尺与空值分支，空值单独进 unknown 盒 | 范围、单位、空值规则都要先定 |
| 07 | `three-methods` | 6–10s | 评分可以来自人工、代码规则或模型评审。不同方法回答的问题和出错方式不一样。 | 三扇门：human / code / LLM judge，各自带不同风险提示 | 人工、代码、模型评分不能混为一谈 |
| 08 | `code-rule` | 6–10s | 代码规则适合明确、可重复的条件，但规则通过不等于语义质量一定好。 | 规则卡 `required fields present?`，旁边语义评价仍留空 | 规则通过 ≠ 语义质量一定好 |
| 09 | `judge-calibration` | 6–10s | 模型评审也需要校准、抽样复核和失败分析，不能因为用了另一个模型就自动可信。 | 评审模型与天平静置，抽样卡逐一翻开 | 模型评审也需要校准和抽查 |
| 10 | `target-map` | 6–10s | 被评对象要固定，可以是 Trace、Observation 或 Dataset run，并保留实际关联标识。 | 对象地图：Trace / Observation / run 连到同一个 Score | 先确认分数到底评的是谁 |
| 11 | `metadata-card` | 6–10s | 一条可复核的 Score，要留下名称、值、数据类型、评分方法版本和运行时间。 | Score 元数据卡逐行点亮，具体字段角标「按当前版本核对」 | 分数之外，还要留评分版本和时间 |
| 12 | `response-ticket` | 6–10s | 写入返回 2xx，只说明观察到了响应。它不能单独证明 Score 已经能回读，更不能证明关联正确。 | 2xx 回执与“已回读”之间放断开的桥 | 写入 2xx ≠ Score 已回读 |
| 13 | `readback-loop` | 6–10s | 用同一个关联 ID 回读 Score 和原始输入输出，核对值、类型、关联关系和时间。 | 闭环：写入 → ID → 回读 → 原始样本，不使用真实 ID | 同一个 ID 回读分数和原始样本 |
| 14 | `high-low-split` | 6–10s | 高分也要抽查，低分也要打开。前者帮你找误判，后者帮你定位真实失败。 | 左高分样本、右低分样本，各放一枚放大镜 | 高低分都要抽查 |
| 15 | `failure-tree` | 6–10s | 看到低分，继续打开对应 Trace，检查失败节点、输入输出和错误，别只截一个数字。 | 低分卡展开成 Trace 树，失败节点标红，所有值为示意 | 低分要回到失败节点和输入输出 |
| 16 | `comparison-board` | 6–10s | 做实验比较时，要固定数据、Prompt、模型和评分规则。只改一个变量，再观察本次差异。 | 对照板四把锁，只有候选变量一项可切换 | 固定条件，只改一个变量再比较 |
| 17 | `cohort-view` | 6–10s | 汇总时同时保留样本量、分组结果和失败类型。一个总分不能代替这些信息。 | 三栏：样本量 / 分组 / 失败类型；总分退到最下 | 总分别离开样本量和失败类型 |
| 18 | `decision-gate` | 6–10s | 高分不等于模型更好、更稳定，也不等于可以上线。发布门还要看预设标准和关键失败。 | 高分卡停在发布闸门前，闸门列出标准与关键失败 | 有分数，不等于通过上线决策 |
| 19 | `stamp` | 6–10s | 本集画面是 prototype、L1 示意，不代表当前实例已完成 Score 写入、Dataset run 或回读。 | PROTOTYPE / L1 印章，写入、run、回读全部标未证明 | prototype / L1：不是评分已跑通 |
| 20 | `cta` | 6–10s | 下一集讲成本、token 和延迟：这些字段从哪里来，又为什么不能只看一个总数？ | LF-07 预告卡：cost / token / latency 三个仪表，值留空 | 下一集：成本、token 和延迟怎么看 |

## 固定构图顺序

`hook → average-mask → score-card → evaluation-cycle → rubric → scale → three-methods → code-rule → judge-calibration → target-map → metadata-card → response-ticket → readback-loop → high-low-split → failure-tree → comparison-board → cohort-view → decision-gate → stamp → cta`

## 字幕与旁白

- 声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`，禁止整段变速。
- 首次出现中英并读：Evaluation 评测、Score 评分、Trace 运行记录、Dataset run 数据集实验运行。
- 烧录字幕使用表中短句；SRT、VTT 使用同一时间轴，最后一条与片尾对齐。
- 不编造真实高分、提升、排名、样本量或模型质量结论。

## 演示与证据边界

1. 录制时保存固定评分对象、规则、范围、单位、空值规则和 evaluator 版本。
2. 保存 Score 写入响应、关联 ID、同 ID 回读和原始输入输出；2xx 不能代替回读。
3. 抽查高分、低分和失败样本，保留样本量、分组与失败类型。
4. 规则评分不是通用质量判断，模型评审也需要校准和复核。
5. 当前文件只定义概念课画面，不证明当前实例评分或实验已运行。

## 官方来源（录制当天复核）

- Evaluation 概览：https://langfuse.com/docs/evaluation/overview
- Scores：https://langfuse.com/docs/observability/features/scores
- Experiments：https://langfuse.com/docs/evaluation/experiments
