# LF-11《用同一 Dataset 比较 Prompt 或模型》Xiaoxiao 分镜板

用途：按 `zh-CN-XiaoxiaoNeural`、`rate=-5%` 为 20 段口播制作画面。口播多长，成片就多长；禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

## 制作规则

- 20 镜使用 20 种不同构图，相邻构图不得重复。
- 每镜画面内只烧一条短字幕，完整口播保留在「口播」列。
- Prompt/模型版本、run ID、分数、成本、延迟和样本结果均为示意或留空。
- 不宣称当前实例已完成两个真实 run，不宣称任何候选全面领先。
- 无内网地址、密钥、Authorization 值、PII、完整 Prompt 或真实业务输入输出。

## 20 镜分镜

| 镜 | 构图 | 时长提示 | 口播 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | 新版本平均分更高，为什么还不能直接上线？因为关键样本可能正在回退。 | 上方平均分箭头向上，下方关键样本由通过变失败 | 平均分更高，也可能藏着关键回退 |
| 02 | `shared-dataset` | 6–10s | 公平比较的第一步，是让两个候选回到同一 Dataset，使用同一组固定输入。 | 同一个 Dataset 卡分流到候选 A 和 B | 两个候选，先用同一组输入 |
| 03 | `item-ids` | 6–10s | 每条 item 要有稳定标识。A 的第一题和 B 的第一题，必须真的是同一条样本。 | A/B 两侧 item 按同一 ID 对齐，错位连接被打叉 | 用稳定 item ID 对齐两条结果 |
| 04 | `rule-lock` | 6–10s | 评分规则也要相同，包括 evaluator 版本、范围、空值和失败判定。 | 评分规则上锁，空值与失败条件单独列出 | 同一评分规则，才有可比起点 |
| 05 | `baseline-candidate` | 6–10s | 先把已审查的基线和候选分清楚。不要跑完以后，才挑一个看起来更好的当基线。 | 已审查 baseline 与 candidate 两张卡，基线不可事后替换 | 基线要先固定，不能事后挑 |
| 06 | `run-a` | 6–10s | 跑基线时，保存 run 标识、逐 item 原始输出、运行时间和版本条件。 | 基线 run 抽屉保存 item 输出、metadata 和时间 | 基线 run 留下逐条原始证据 |
| 07 | `run-b` | 6–10s | 跑候选时只改一个变量。比较 Prompt 就固定模型，比较模型就固定 Prompt 和参数。 | 候选 run 只高亮一个变化项，其余配置锁定 | 比较谁，就只改变谁 |
| 08 | `pair-table` | 6–10s | 先逐 item 看输入、两个输出和分数变化，再看汇总。这样才知道差异发生在哪里。 | 成对对照表：item / baseline / candidate / change | 先逐样本对照，再看汇总 |
| 09 | `regression-spotlight` | 6–10s | 单独展开由通过变失败的样本。平均分上涨，不能抵消关键场景回退。 | 回归样本被聚光灯放大，平均分隔到背景 | 通过变失败的样本必须单独展开 |
| 10 | `missing-gate` | 6–10s | 缺失 case、任务失败或没有评分结果，都不能当成成功。先解释缺口，再决定能否比较。 | 发布门前三类缺口：missing / failed / no score | 缺失、失败、无评分都不能放行 |
| 11 | `null-handling` | 6–10s | 空值不要悄悄算成零分，也不要从分母里删掉。按预先写好的规则处理。 | 空值进入单独处理路径，零分与删除路径均打叉 | 空值按规则处理，不能偷偷改分母 |
| 12 | `cohort-bars` | 6–10s | 按场景分组看差异，并保留每组样本量。总体上涨可能来自样本结构，而不是每组都变好。 | 分组条形图旁边标样本量，具体数值留空 | 分组结果必须带样本量 |
| 13 | `repeat-runs` | 6–10s | 模型有波动，单次差异不一定稳定。需要重复运行或其他统计依据时，就不能只讲一次结果。 | 多次运行点围绕两条分布，差异区间未计算前留空 | 一次差异，不等于稳定差异 |
| 14 | `cost-latency` | 6–10s | 成本和延迟也要在同样条件下比较。字段缺失就写 unknown，不能用单条结果推出长期 P95。 | cost / latency 双卡，unknown 与 P95 未证明同时可见 | 成本、延迟也要同条件、可回读 |
| 15 | `metadata` | 6–10s | 两次 run 都要保留 Dataset 版本、Prompt、模型、参数、SDK、代码版本和运行时间。 | 元数据矩阵逐项对应 A/B，commit 用脱敏占位 | 两次 run 的版和条件都要留下 |
| 16 | `readback-loop` | 6–10s | 最后用同一 run 和 item 关联回读 Score、输出和失败类型，确认没有串到历史记录。 | 两次 run 各自进入同轮回读闭环 | 按同一 run、item 回读结果 |
| 17 | `bounded-claim` | 6–10s | 结论只能说：在这组数据、这些版本和这些条件下，观察到了什么。不要扩成全面领先。 | 结论卡被套在数据、版本、条件三层边界框内 | 结论只适用于本次数据和条件 |
| 18 | `stats-gate` | 6–10s | 没有样本量、波动或置信区间依据，就不要说统计显著。观察到差异和证明显著是两回事。 | “观察到差异”与“统计显著”两道门分开 | 观察到差异 ≠ 统计显著 |
| 19 | `stamp` | 6–10s | 本集画面是 prototype、L1 示意，不代表当前实例已完成两个 run 或 Score 回读。 | PROTOTYPE / L1 印章，run A/B 和 Score 均标未证明 | prototype / L1：不是实验比较已完成 |
| 20 | `cta` | 6–10s | 下一集讲异常 Trace：发现回退后，怎样从失败样本定位、修复，再做回归？ | LF-12 预告卡：异常 Trace → 修复 → 回归闭环 | 下一集：从异常 Trace 到修复和回归 |

## 固定构图顺序

`hook → shared-dataset → item-ids → rule-lock → baseline-candidate → run-a → run-b → pair-table → regression-spotlight → missing-gate → null-handling → cohort-bars → repeat-runs → cost-latency → metadata → readback-loop → bounded-claim → stats-gate → stamp → cta`

## 字幕与旁白

- 声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`，禁止整段变速。
- 首次出现保留英文并给中文解释：Dataset 数据集、run 实验运行、Score 评分、baseline 基线。
- 烧录字幕使用表中短句；SRT、VTT 使用同一时间轴，最后一条与片尾对齐。
- 不编造分数、提升比例、成本、延迟、样本量、置信区间或排名。

## 演示与证据边界

1. 保存 Dataset 版本、稳定 item ID、两个 run 及逐 item 原始输出。
2. 固定评分规则和 evaluator 版本，保留空值、缺失、失败和分组结果。
3. 成本/延迟缺失写 unknown；统计结论需要明确方法，不能由一次运行推出。
4. 两个 run 都需当前版本支持的 UI/API 回读，并核对关联关系。
5. 当前文件只定义概念课画面，不证明当前实例实验已完成或候选更好。

## 官方来源（录制当天复核）

- Experiments：https://langfuse.com/docs/evaluation/experiments
- Prompt Management：https://langfuse.com/docs/prompt-management
