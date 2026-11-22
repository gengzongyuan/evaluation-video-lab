# LF-23《自定义 Score 到 Dataset 回归样本》Xiaoxiao 分镜板

用途：按 `zh-CN-XiaoxiaoNeural`、`rate=-5%` 为 20 段口播制作画面。口播多长，成片就多长；禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

## 制作规则

- 20 镜使用 20 种不同构图，相邻构图不得重复。
- 每镜画面内只烧一条短字幕，完整口播保留在「口播」列。
- Score、Trace、run、item 和回归结果均为示意或留空。
- 无内网地址、真实 key/secret、Authorization 值、PII 或未脱敏 Prompt。

## 20 镜分镜

| 镜 | 构图 | 时长提示 | 口播 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | 看到低分样本，别急着全塞进 Dataset。先问：它能不能成为一条可复跑的回归用例？ | 低分样本冲向 Dataset，中央闸门写“可复跑？” | 低分样本，先别直接入库 |
| 02 | `filter-map` | 6–10s | 自定义 Score 可以帮你筛选候选，比如按名称、来源、数值或配置 ID 找样本。分数只是入口，不是根因。 | Score 字段映射到候选筛选器，根因区仍标未知 | Score 是筛选入口，不是根因 |
| 03 | `score-config` | 6–10s | 筛选前先固定 Score 定义。配置不可变；同名分数若关联不同配置，就不能直接当成同一种失败。 | 同名 Score 关联不同 configId，禁止直接合并 | 同名分数，也要核对配置 ID |
| 04 | `missing-score` | 6–10s | 没有 Score 的样本单独标成 unknown。缺失可能来自没评、评估失败或关联缺失，不能自动当零分。 | 空 Score 卡进入 unknown 分支，零分分支断开 | 缺失写 unknown，不自动当零分 |
| 05 | `three-buckets` | 6–10s | 候选池别只收低分。保留通过样本和边界案例，才能检查修复有没有误伤原本正确的行为。 | 失败、正例、边界三个样本桶并列进入候选池 | 失败、正例、边界都要保留 |
| 06 | `candidate-queue` | 6–10s | 把候选放进待审核队列，先记录筛选条件和抽样范围。不要从一次 run 推成整体质量结论。 | 候选队列顶部固定筛选条件与范围，整体结论留空 | 记录筛选条件，不外推整体质量 |
| 07 | `trace-back` | 6–10s | 每条候选回到原始 Trace 或实验 item，核对输入、输出、上下文和 Score 是否属于同一次运行。 | 候选卡反向连接 Trace、item、输入输出与 Score | 回到同一次运行核对证据 |
| 08 | `sanitize` | 6–10s | 进入 Dataset 前先做脱敏和权限检查。密钥、个人信息、内部地址和完整敏感 Prompt 都不能直接入库。 | 原始内容经过脱敏与权限两道门，敏感字段以遮罩表示 | 入库前，先脱敏并检查权限 |
| 09 | `expected-actual` | 6–10s | 样本结构要把输入、期望输出和本次实际输出分开。Dataset 存输入与期望，实际输出保留在运行证据里。 | Dataset item 与运行结果分栏，期望值和实际输出不混写 | 期望值与实际输出分开保存 |
| 10 | `lineage-links` | 6–10s | 同时保留来源关联：Trace、run、item、Score 和筛选规则版本。后面才能解释它为什么被选入。 | 五类关联沿样本血缘链排列，筛选规则带版本号 | 保留来源关联和筛选规则版本 |
| 11 | `dedupe` | 6–10s | 相似失败不等于可以无限复制。按规范化输入和失败特征去重，同时保留必要的不同上下文。 | 相似候选聚类去重，不同上下文分支被保留 | 相似失败去重，保留必要差异 |
| 12 | `review-gate` | 6–10s | 入库前由人审核期望值、标签和适用范围。自动低分可以排队，不能自动宣布标准答案。 | 人工审核门检查期望值、标签、范围，自动低分停在门外 | 自动低分，不能自动成为标准答案 |
| 13 | `dataset-schema` | 6–10s | 审核通过后再创建 Dataset item。字段、标签和元数据保持明确，缺失信息不要为了好看而补齐。 | Dataset item 表单含输入、期望、标签、元数据，未知字段留空 | 审核通过，再创建 Dataset item |
| 14 | `version-pin` | 6–10s | 记录 Dataset 的版本时间戳和评测配置。后续重跑才能区分，结果变化来自模型、数据还是评估规则。 | Dataset 版本时间戳与评测配置锁定，模型变化单独对照 | 固定 Dataset 版本和评测配置 |
| 15 | `baseline-rerun` | 6–10s | 用固定模型、Prompt、工具和数据版本重跑，再与基线比较。条件变了，就先分开报告。 | 基线与重跑双泳道，固定条件逐项锁定 | 固定条件重跑，再比较基线 |
| 16 | `regression-matrix` | 6–10s | 回归结果至少看三类：原失败是否改善、原通过是否回退、边界样本是否仍稳定。别只看均分。 | 三行回归矩阵：失败改善、正例回退、边界稳定 | 看改善、回退和边界，不只看均分 |
| 17 | `new-failure` | 6–10s | 出现新增失败或关键回退时，回到具体 item 和 Trace 排查。汇总变好，也不能掩盖这些样本。 | 上升汇总曲线旁突出新增失败，钻取到 item 与 Trace | 汇总变好，也不能放过关键回退 |
| 18 | `scope-boundary` | 6–10s | 这批样本来自哪里、筛选了什么，就只对哪个范围负责。候选集不是随机抽样，也不代表总体满意度。 | 候选集边界圈住来源与筛选条件，总体结论置于圈外 | 候选集有边界，不代表总体满意 |
| 19 | `stamp` | 6–10s | 本集是 prototype、L1 示意，没有执行真实 Score 筛选、Dataset 写入、回读或回归运行。 | PROTOTYPE / L1 印章，筛选、写入、回读、重跑均标未证明 | prototype / L1：未执行真实入库与回归 |
| 20 | `cta` | 6–10s | 下一集用一条完整链路串起来：从 Trace 到 Score，再到 Dataset 和可重复的 Experiment。 | LF-24 预告：Trace → Score → Dataset → Experiment | 下一集：串起可重复的评测链路 |

## 固定构图顺序

`hook → filter-map → score-config → missing-score → three-buckets → candidate-queue → trace-back → sanitize → expected-actual → lineage-links → dedupe → review-gate → dataset-schema → version-pin → baseline-rerun → regression-matrix → new-failure → scope-boundary → stamp → cta`

## 字幕与旁白

- 声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`，禁止整段变速。
- 首次出现中英并读：Score 评分、Dataset 数据集、Trace 追踪、run 运行、item 样本、Experiment 实验。
- 烧录字幕使用表中短句；SRT、VTT 使用同一时间轴，最后一条与片尾对齐。
- 不编造真实筛选数量、入库数量、回归改善率、模型质量或总体满意度。

## 演示与证据边界

1. Score 只用于候选筛选；缺失分数写 `unknown`，不把缺失自动当零分或失败根因。
2. 候选同时保留失败、正例和边界样本；入库前完成原运行核对、脱敏、权限检查、去重与人工审核。
3. Dataset item 的输入与期望输出同本次实际输出分开；保留 Trace、run、item、Score 和筛选规则版本关联。
4. 回归比较固定模型、Prompt、工具、Dataset 版本时间戳和评测配置；新增失败与关键回退必须下钻，不用均分掩盖。
5. 当前文件只定义概念课画面，不证明已执行真实 Score 筛选、Dataset 写入、回读或 Experiment。

## 官方来源（录制当天复核）

- Scores 数据模型：https://langfuse.com/docs/evaluation/scores/data-model
- Experiments 数据模型：https://langfuse.com/docs/evaluation/experiments/data-model
- Datasets：https://langfuse.com/docs/evaluation/experiments/datasets
- Academy｜Datasets：https://langfuse.com/academy/datasets
