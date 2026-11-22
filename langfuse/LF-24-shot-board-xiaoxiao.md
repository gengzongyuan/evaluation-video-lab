# LF-24《Trace 到 Experiment 的完整评测链路》Xiaoxiao 分镜板

用途：按 `zh-CN-XiaoxiaoNeural`、`rate=-5%` 为 20 段口播制作画面。口播多长，成片就多长；禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

## 制作规则

- 20 镜使用 20 种不同构图，相邻构图不得重复。
- 每镜画面内只烧一条短字幕，完整口播保留在「口播」列。
- Trace、Score、Dataset、run、item 和实验结果均为示意或留空。
- 无内网地址、真实 key/secret、Authorization 值、PII 或未脱敏 Prompt。

## 20 镜分镜

| 镜 | 构图 | 时长提示 | 口播 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | 一次实验结束，页面上有了总分，链路就算闭环了吗？还不够。先确认每个对象都能沿着同一关联找回来。 | 总分旁出现断开的关联链，中央问号“能追回？” | 有总分，不等于证据闭环 |
| 02 | `object-map` | 6–10s | 完整链路包含生产 Trace、Score、Dataset item、Experiment run，以及 run 产生的新 Trace。对象不同，关联不能靠猜。 | 五类对象分层排列，原 Trace 与新 Trace 使用不同颜色 | 先分清对象，再连接证据 |
| 03 | `production-trace` | 6–10s | 起点是一条已脱敏、获准使用的生产 Trace。它记录原始输入输出和中间步骤，是候选证据，不是标准答案。 | 生产 Trace 树经过脱敏标记，标准答案区域留空 | 生产 Trace 是候选，不是标准答案 |
| 04 | `score-inspector` | 6–10s | Score 告诉我哪里值得检查。先看名称、来源、类型和 configId，再决定筛选规则，不能只拿一个数字排队。 | Score 检查器展开 name、source、dataType、configId | 筛选前，先检查 Score 定义 |
| 05 | `review-split` | 6–10s | 低分先由人复核。区分应用失败、评估器错误和缺失结果；评估器没跑完，不能记成不通过。 | 低分进入三路复核：应用、评估器、缺失结果 | 应用失败与评估器错误要分开 |
| 06 | `item-builder` | 6–10s | 审核后，把输入和可选的期望输出整理成 Dataset item。生产实际输出不应未经审核直接变成期望值。 | 输入与期望输出分栏组装 item，实际输出经过审核门 | 实际输出不能自动成为期望值 |
| 07 | `source-link` | 6–10s | 用 sourceTraceId，必要时加 sourceObservationId，保留 item 的来源。其他筛选理由和版本信息可放 metadata。 | item 通过两个来源字段连回 Trace，metadata 单独收纳 | 用来源字段保留样本血缘 |
| 08 | `version-timeline` | 6–10s | 固定 Dataset 版本时间戳。新增、修改、删除或归档 item 都会形成新版本，latest 不等于本次基线。 | item 变更生成版本时间线，基线固定在一个时间点 | 固定版本时间戳，不追 latest |
| 09 | `creation-paths` | 6–10s | 创建 Experiment 可走 SDK、UI 或 OpenTelemetry。当前没有公开 REST 端点用来创建新 run，旧写入路径已废弃。 | 三条有效创建路径高亮，旧 REST 路径标 deprecated | 创建 run 走 SDK、UI 或 OTEL |
| 10 | `runner-loop` | 6–10s | Experiment runner 逐个执行 Dataset item，调用你的任务函数，再运行 item 级评估器。每个任务执行都有可排查的 Trace。 | runner 循环：item → task → evaluator → 新 Trace | 每个 item 都留下执行 Trace |
| 11 | `run-item-triangle` | 6–10s | 每个 DatasetRunItem 关联 run、Dataset item 和新 Trace。核对这三个 ID，才能把输出归到正确的实验样本。 | run、item、Trace 三角关联，中心为 DatasetRunItem | 核对 run、item、Trace 三个关联 |
| 12 | `item-evaluator` | 6–10s | item 级评估器接收输入、输出、期望输出和 metadata，返回的 Evaluation 会成为 Trace 上的 Score。 | 四类输入进入 item 评估器，Evaluation 落到新 Trace | item 级 Evaluation 成为 Trace Score |
| 13 | `run-evaluator` | 6–10s | run 级评估器看整轮结果，产生的 Score 关联 DatasetRun。它和 item 级分数的层级不同，不要混在一张表里。 | item 分数与 run 分数分层归位，汇总表分开 | item 级与 run 级分数分层保存 |
| 14 | `flush-readback` | 6–10s | 程序返回不等于数据已可读。完成 flush 或 shutdown 后，再用 Experiments API 回读 run、item、Score、错误和时间。 | 运行结束后经 flush/shutdown，再进入 API 回读清单 | 程序返回后，还要 flush 并回读 |
| 15 | `completeness-audit` | 6–10s | 先核对样本完整性：该跑的 item 是否都有结果，失败和缺失是否单独列出。缺失 case 不能算 pass。 | item 清单逐条对账，失败、缺失、通过分列 | 缺失 case 不能算通过 |
| 16 | `baseline-select` | 6–10s | 比较时选定已审核的基线 run，固定同一 Dataset 版本和评估器定义。最新 run 不会自动成为获批基线。 | 基线选择卡与候选 run 对照，latest 标签被移开 | 基线要审核，不自动选最新 run |
| 17 | `metadata-card` | 6–10s | 把应用 commit、Prompt 或模型版本、评估器版本写进实验 metadata。Dataset 固定了，也不代表模型输出完全确定。 | 实验 metadata 卡固定 commit、Prompt、模型与评估器 | 固定数据，也不保证输出确定 |
| 18 | `regression-drilldown` | 6–10s | 先看汇总，再下钻新增失败和关键回退。并排检查基线与候选输出，最后打开 Trace 找原因。 | 汇总 → 回退样本 → 双输出对照 → Trace 四级下钻 | 从汇总下钻到回退和 Trace |
| 19 | `stamp` | 6–10s | 本集仍是 prototype、L1 概念演示。没有真实凭据、run、Score 写入或同 run 回读，就不能说链路已跑通。 | PROTOTYPE / L1 印章，run、Score、回读均标未证明 | prototype / L1：完整链路尚未运行 |
| 20 | `cta` | 6–10s | 下一集讲如何把这些证据变成发布门：必需样本、关键回退和不完整结果，怎样阻止一次错误上线。 | LF-25 预告：必需样本、关键回退、不完整结果进入发布门 | 下一集：把实验证据变成发布门 |

## 固定构图顺序

`hook → object-map → production-trace → score-inspector → review-split → item-builder → source-link → version-timeline → creation-paths → runner-loop → run-item-triangle → item-evaluator → run-evaluator → flush-readback → completeness-audit → baseline-select → metadata-card → regression-drilldown → stamp → cta`

## 字幕与旁白

- 声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`，禁止整段变速。
- 首次出现中英并读：Trace 追踪、Score 评分、Dataset 数据集、Experiment 实验、run 运行、item 样本、metadata 元数据。
- 烧录字幕使用表中短句；SRT、VTT 使用同一时间轴，最后一条与片尾对齐。
- 不编造真实 run ID、样本数量、实验分数、回退数量、模型质量或发布结论。

## 演示与证据边界

1. 原生产 Trace 与 Experiment 产生的新 Trace 分开；Score 只提示候选，实际输出须经审核才能成为期望输出。
2. Dataset item 用来源字段连接原 Trace，并固定 Dataset 版本时间戳；latest 不等于已审核基线。
3. Experiment 创建走 SDK、UI 或 OpenTelemetry；程序返回后完成 flush/shutdown，再回读同一 run 的对象与错误。
4. item 级 Score 关联 Trace，run 级 Score 关联 DatasetRun；缺失 case、评估器错误与关键回退均不得隐藏。
5. 当前文件只定义概念课画面，不证明真实 Experiment、Score 写入、回读或发布门已执行。

## 官方来源（2026-11-23 已读取，录制当天仍需复核）

- Scores 数据模型：https://langfuse.com/docs/evaluation/scores/data-model
- Experiments 数据模型：https://langfuse.com/docs/evaluation/experiments/data-model
- Datasets：https://langfuse.com/docs/evaluation/experiments/datasets
- Experiments via SDK：https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk
- Compare experiments：https://langfuse.com/docs/evaluation/experiments/compare-experiments
