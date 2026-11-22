# LF-21《Dataset Run、Score 写入与实验回读》Xiaoxiao 分镜板

用途：按 `zh-CN-XiaoxiaoNeural`、`rate=-5%` 为 20 段口播制作画面。口播多长，成片就多长；禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

## 制作规则

- 20 镜使用 20 种不同构图，相邻构图不得重复。
- 每镜画面内只烧一条短字幕，完整口播保留在「口播」列。
- run、Score、样本、版本、响应和汇总均为示意或留空。
- 不伪造真实运行、分数、写入响应、回读或比较结论。
- 无内网地址、真实 key/secret、Authorization 值、登录信息、PII 或未脱敏 Prompt。

## 20 镜分镜

| 镜 | 构图 | 时长提示 | 口播 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | 跑完一次评测，先看平均分吗？先别急。先确认这一轮的 run、样本、Score 和回读能不能对上。 | 平均分退到背景，run / item / Score / readback 四个未知关系前置 | 先看证据闭环，再看平均分 |
| 02 | `flow` | 6–10s | 整集只走一条链：冻结 Dataset，创建 run，逐条写 Score，再按同一个 run 回读。 | Dataset → run → Score → readback 四步流程 | Dataset → run → Score → 同一轮回读 |
| 03 | `freeze` | 6–10s | 先固定 Dataset 版本和测试题。它只固定输入集合，不保证模型输出每次都一样。 | Dataset 版本章与输出波动符号同时出现 | 固定 Dataset，不等于固定模型输出 |
| 04 | `run-card` | 6–10s | run 是这次执行的身份。保存 run ID、Prompt/模型版本、参数、SDK、代码版本和时间。 | run 元数据卡逐项点亮，标识使用脱敏占位 | run 要能回指版本、参数和时间 |
| 05 | `new-run` | 6–10s | 任何比较条件变了，都应该产生新 run，而不是覆盖旧结果。旧 run 是复核基线的一部分。 | 条件变化生成新 run，旧 run 保留不被覆盖 | 条件变了就新建 run，不覆盖旧结果 |
| 06 | `create-paths` | 6–10s | 创建实验 run 走当前 SDK、UI 或 OTEL 路径。没有用于创建新 experiment run 的公开 REST 端点。 | 三条创建路径并列，旧 dataset-run-items POST 标已废弃 | 创建 run 走 SDK、UI 或 OTEL |
| 07 | `item-table` | 6–10s | 执行每条 item 时，保存稳定 item ID、run ID、原始输出和状态。失败不能被静默丢掉。 | item 表逐行关联 run，失败行保留且标红 | 每条输出和失败都要绑定 item、run |
| 08 | `score-types` | 6–10s | Score 可以是数值、分类、布尔或文本。不是所有分数都有数值，不同类型不能混算。 | numeric / categorical / boolean / text 四种类型卡 | Score 有不同类型，不能混算 |
| 09 | `source-lanes` | 6–10s | Score 的底层来源分 API、EVAL、ANNOTATION。自动评测、人工标注和 API 写入要分开看。 | 三条来源泳道，来源字段不由口播随意命名 | Score 来源分 API、EVAL、ANNOTATION |
| 10 | `evaluator-card` | 6–10s | 还要记录评分名称、范围、空值规则、评估器版本和关联对象，否则分数很难复核。 | evaluator 卡连接 score / item / run 与版本 | 评分规则、版本和关联对象都要留下 |
| 11 | `score-write` | 6–10s | 新代码写入 Score 使用当前官方 `POST /api/public/scores` 路径，字段以录制当天文档为准。 | Score 写入卡连接当前 API 文档，payload 脱敏 | Score 写入路径按当前官方文档核对 |
| 12 | `response-boundary` | 6–10s | 写入响应只说明观察到了返回，不等于同一 run 的结果已能回读，更不等于实验已通过。 | 写入回执停在回读门前，实验通过区为空 | Score 写入响应 ≠ 实验已回读 |
| 13 | `experiment-readback` | 6–10s | 用当前 Experiments API 回读同一 run 的 item、输出、错误和时间戳，确认属于这一轮。 | 同一 run ID 进入 Experiments API 回读清单 | 用同一 run ID 回读实验结果 |
| 14 | `score-readback` | 6–10s | Score 再用当前 v3 scores 读取，逐条核对 item、值或分类、来源和关联关系。 | Score 回读卡逐字段匹配 run/item/source | 逐条回读 Score 和它的关联对象 |
| 15 | `time-check` | 6–10s | 写入、回读和运行时间要能对应。历史截图、旧 run 或空 POST 的 401 都不能补这次证据。 | 同轮时间窗与历史记录隔离，401 不能进入证据包 | 排除旧 run，只核对本轮新证据 |
| 16 | `aggregate-gate` | 6–10s | 先逐条看完输入、输出、Score 和失败，再看汇总。缺失、报错和无评分不能算通过。 | 逐条复核门通过后才允许进入汇总视图 | 先逐条复核，再看汇总 |
| 17 | `compare-board` | 6–10s | 比较两个 Prompt 或模型时，Dataset、评分规则和统计口径必须相同，结论只覆盖本次条件。 | A/B 对照板共享同版数据与评分，结论框有限定 | 同条件比较，结论不超出本次范围 |
| 18 | `evidence-pack` | 6–10s | 最小证据包要包含 run 元数据、脱敏 payload、写入响应、Score 记录、同轮回读和 hash 清单。 | 六件证据装入同一证据包，缺件时标 BLOCKED | 六件证据齐全，才申请升级证据等级 |
| 19 | `stamp` | 6–10s | 本集画面是 prototype、L1 示意。当前 Dataset run、Score 写入、回读和比较结论全部 BLOCKED。 | PROTOTYPE / L1 印章，四类运行结论均标 BLOCKED | prototype / L1：真实 run 和回读仍 BLOCKED |
| 20 | `cta` | 6–10s | 到这里，从 Trace 到实验回读的主线就串起来了。下一次复现，从一条脱敏样本和同 ID 回读开始。 | 全系列路线收束为一条可执行动作：固定样本 → 运行 → 回读 | 从一条脱敏样本和同 ID 回读开始 |

## 固定构图顺序

`hook → flow → freeze → run-card → new-run → create-paths → item-table → score-types → source-lanes → evaluator-card → score-write → response-boundary → experiment-readback → score-readback → time-check → aggregate-gate → compare-board → evidence-pack → stamp → cta`

## 字幕与旁白

- 声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`，禁止整段变速。
- 首次出现中英并读：Dataset 数据集、run 实验运行、Score 评分、readback 回读。
- 烧录字幕使用表中短句；SRT、VTT 使用同一时间轴，最后一条与片尾对齐。
- 不编造真实 run ID、Score、样本量、响应、统计显著或模型排名。

## 演示与证据边界

1. run 创建走 SDK/UI/OTEL，读取走当前 Experiments API；Score 读取走 v3 scores。
2. Score 来源为 API/EVAL/ANNOTATION，类型与来源不能混算。
3. 逐条保存 item/run/output/status、Score、错误和时间；失败不能静默丢弃。
4. 同一轮六件证据齐全才申请升级；缺真实凭据时全部保持 `BLOCKED`。
5. 当前文件只定义概念课画面，不证明当前实例 run、Score 或实验比较已完成。

## 官方来源（录制当天复核）

- Scores 数据模型：https://langfuse.com/docs/evaluation/scores/data-model
- Experiments 数据模型：https://langfuse.com/docs/evaluation/experiments/data-model
- v4 API 迁移索引：https://langfuse.com/llms.txt
