# LF-22《Annotation Score 与 Evaluation Score》Xiaoxiao 分镜板

用途：按 `zh-CN-XiaoxiaoNeural`、`rate=-5%` 为 20 段口播制作画面。口播多长，成片就多长；禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

## 制作规则

- 20 镜使用 20 种不同构图，相邻构图不得重复。
- 每镜画面内只烧一条短字幕，完整口播保留在「口播」列。
- 分数、标注人、评估器和样本结果均为示意或留空。
- 无内网地址、真实 key/secret、Authorization 值、PII 或未脱敏 Prompt。

## 20 镜分镜

| 镜 | 构图 | 时长提示 | 口播 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | 人工给了差评，自动评估却给了高分，谁一定对？都不一定。先看分数从哪里来。 | 人工低分与自动高分碰撞，中央问号“来源？” | 分数冲突时，先看评分来源 |
| 02 | `same-score` | 6–10s | Annotation Score 和 Evaluation Score 都可以是 Score 对象。它们最直观的区别，是产生方式和用途。 | 两个分数汇入同一 Score 模型，来源字段分叉 | 都是 Score，来源和用途不同 |
| 03 | `source-lanes` | 6–10s | 官方 Score 来源分 API、EVAL、ANNOTATION。人工标注对应 ANNOTATION，评测结果对应 EVAL。 | 三条来源泳道，ANNOTATION 与 EVAL 分别高亮 | 人工标注和自动评测，来源字段不同 |
| 04 | `annotation-card` | 6–10s | 人工标注让人按明确标准检查一条运行，适合语义、偏好和失败原因这些难完全规则化的判断。 | 人工标注卡：样本 / 标准 / 评分 / 评论 | 人工标注适合需要判断的样本 |
| 05 | `evaluation-card` | 6–10s | Evaluation Score 来自代码规则、模型评审或其他评估流程，适合按同一方法批量产生结果。 | 评估器卡批量处理样本，规则版本明确 | 自动评估适合按同一方法批量评分 |
| 06 | `api-source` | 6–10s | API 来源不等于人工评分。通过接口写入的外部结果，也要单独保留来源和定义。 | API 写入卡独立于 ANNOTATION 和 EVAL | API 写入，不等于人工标注 |
| 07 | `type-grid` | 6–10s | 无论来源是什么，分数还可能是数值、分类、布尔或文本。来源和类型是两个维度。 | 来源与类型二维矩阵，避免把二者混成一个字段 | 来源是一维，分数类型是另一维 |
| 08 | `rubric` | 6–10s | 人工评分也需要清晰标准、示例和空值规则。让标注员凭感觉打分，结果很难复查。 | 标注规范卡：定义 / 示例 / 空值 / 失败判定 | 人工评分也需要明确 rubric |
| 09 | `judge-calibration` | 6–10s | 自动评分也需要校准。模型评审说得再完整，都不能自动成为客观真值。 | 自动评审与人工复核校准秤，结论待验证 | 自动评审不等于客观真值 |
| 10 | `human-boundary` | 6–10s | 人工也会误解、疲劳或标准不一致。人工分数是可追溯判断，不是永远正确的答案。 | 人工标注卡旁列误解、疲劳、标准差异三类风险 | 人工分数也不是绝对真值 |
| 11 | `compare-pair` | 6–10s | 比较人工和自动分数时，必须评同一条样本、同一个定义。对象或规则不同，分数差就不能直接解释。 | 同一 item 与同 rubric 连接两个分数 | 同一样本、同一规则，才比较分数 |
| 12 | `disagreement` | 6–10s | 分数不一致时，把分歧样本单独拿出来复核，看是标注错误、规则漏洞，还是模型评审偏差。 | 分歧样本进入仲裁通道，三种可能并列 | 分歧样本是校准评估器的入口 |
| 13 | `agreement` | 6–10s | 多位标注者的一致性可以说明标准执行是否稳定，但它不是模型质量分，也不保证标准本身正确。 | 一致性仪表与模型质量仪表分开 | 标注一致性 ≠ 模型质量 |
| 14 | `aggregate-split` | 6–10s | 汇总时别把人工、自动和 API 分数混成一个平均数。先按来源、名称和定义分组。 | 汇总前按 source/name/definition 分组 | 不同来源和定义，不直接混算 |
| 15 | `comment` | 6–10s | 评论能解释为什么扣分，比单独一个数字更适合复核。评论也可能含敏感信息，公开前要脱敏。 | 分数旁展开脱敏评论，原始用户内容不出现 | 保留评分理由，同时做好脱敏 |
| 16 | `metadata` | 6–10s | 每个 Score 都要保留关联对象、评分名称、来源、评估器或标注规范版本和时间。 | Score 元数据卡逐项核对版本与时间 | 让分数能追回对象、来源和版本 |
| 17 | `readback-loop` | 6–10s | 写入后用同一 Trace、Observation 或 run 关联回读，确认这条 Score 确实属于本次样本。 | 关联 ID → Score → 原始样本回读闭环 | 同一关联 ID 回读 Score 和样本 |
| 18 | `decision` | 6–10s | 最后再用两类分数做不同决策：人工帮助审标准，自动帮助扩大覆盖。谁都不能单独替上线拍板。 | 人工审查与自动覆盖汇入决策门，门仍需标准 | 人工与自动互补，不能单独决定上线 |
| 19 | `stamp` | 6–10s | 本集画面是 prototype、L1 示意，不代表当前实例已产生人工或自动 Score，也没有完成回读。 | PROTOTYPE / L1 印章，两类 Score 与回读均标未证明 | prototype / L1：不是评分流程已运行 |
| 20 | `cta` | 6–10s | 下一集讲自定义 Score 怎样筛出失败样本，再回流成 Dataset 里的回归用例。 | LF-23 预告：Score 筛选 → 失败样本 → Dataset | 下一集：从自定义 Score 到回归样本 |

## 固定构图顺序

`hook → same-score → source-lanes → annotation-card → evaluation-card → api-source → type-grid → rubric → judge-calibration → human-boundary → compare-pair → disagreement → agreement → aggregate-split → comment → metadata → readback-loop → decision → stamp → cta`

## 字幕与旁白

- 声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`，禁止整段变速。
- 首次出现中英并读：Score 评分、Annotation 人工标注、Evaluation 评测、rubric 评分标准。
- 烧录字幕使用表中短句；SRT、VTT 使用同一时间轴，最后一条与片尾对齐。
- 不编造真实分数、标注一致性、自动评审准确率或上线结论。

## 演示与证据边界

1. Score 来源区分 API/EVAL/ANNOTATION；来源与 numeric/categorical/boolean/text 类型分开。
2. 人工与自动评分都需要标准、校准、版本、抽样和失败复核。
3. 比较前固定同一样本与定义，分歧单独审查，汇总按来源和定义分组。
4. 用同一关联 ID 回读 Score 和原始样本；当前无真实运行证据。
5. 当前文件只定义概念课画面，不证明人工或自动评分已执行。

## 官方来源（录制当天复核）

- Scores 数据模型：https://langfuse.com/docs/evaluation/scores/data-model
- Evaluation methods：https://langfuse.com/docs/evaluation/evaluation-methods/overview
- Scores：https://langfuse.com/docs/observability/features/scores
