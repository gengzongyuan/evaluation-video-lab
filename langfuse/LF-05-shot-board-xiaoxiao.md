# LF-05《Dataset 与可重复实验》Xiaoxiao 分镜板

用途：按 `zh-CN-XiaoxiaoNeural`、`rate=-5%` 为 20 段口播制作画面。口播多长，成片就多长；禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

## 制作规则

- 20 镜使用 20 种不同构图，相邻构图不得重复。
- 每镜画面内只烧一条短字幕，完整口播保留在「口播」列。
- Dataset、item、run、Score、Prompt 版本及所有数字均为课程示意。
- 不宣称当前项目已创建 Dataset、完成 run、写入 Score 或回读实验。
- 无内网地址、密钥、Authorization 值、PII 或真实业务输入输出。

## 20 镜分镜

| 镜 | 构图 | 时长提示 | 口播 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | 同一段演示这次变好了，可能只是换了一条更简单的题。怎么重复比较？先看 Dataset。 | 两个 Demo 输出并列，输入难度标签不同；中央大字「换题了？」 | 一条漂亮样例，不等于可重复结论 |
| 02 | `two-demo` | 6–10s | 只拿一条样例说 Prompt 或模型更好，既看不到失败面，也无法排除输入变化。 | 左侧单条高分样例放大，右侧被遮住的失败样本区 | 单条样例，解释不了整体差异 |
| 03 | `dataset-card` | 6–10s | Dataset 先把一组测试输入集中保存，让不同实验能回到同一组题。 | 数据集卡 `intro-demo-v1`（示意）包住三张输入卡 | Dataset：让实验回到同一组题 |
| 04 | `item-grid` | 6–10s | 每一条样本叫 item。输入要脱敏，期望输出或参考信息按实验目标记录。 | 三行 item 网格：input / expected_output / metadata，不填真实内容 | 每条 item 都有输入和明确的参考信息 |
| 05 | `id-tag` | 6–10s | 给 item 保留稳定标识、来源和版本信息，后续才能把结果追回原样本。 | 样本标签卡：`item_demo_01`，连接来源与版本栏 | 结果要能追回原来的 item |
| 06 | `input-output` | 6–10s | 输入和期望结果不是一回事。模型实际输出要单独保存，不能拿期望值覆盖它。 | 三栏：input / expected / actual，actual 栏独立存放 | 期望结果不能覆盖实际输出 |
| 07 | `freeze-board` | 6–10s | 跑实验前，冻结 Dataset、Prompt、模型、参数和评分规则，把运行条件写清楚。 | 五块锁定板围绕一个运行配置，不显示虚构数字 | 先冻结数据和运行条件 |
| 08 | `run-first` | 6–10s | 先用 Prompt v1 跑同一组 item，保存 run 标识、原始输出和每条关联记录。 | 第一条跑道 v1，三个 item 汇入 run；保留原始输出抽屉 | 第一次 run 保存原始输出和关联记录 |
| 09 | `single-variable` | 6–10s | 比较 Prompt 时，只改 Prompt 版本。模型、参数、数据和评分规则保持不变。 | 控制台只有 Prompt v1 → v2 可动，其余四把锁 | 只改一个变量，差异才有解释起点 |
| 10 | `run-second` | 6–10s | 再用 Prompt v2 跑同一 Dataset，得到第二个 run。两次运行要保留各自条件和时间。 | 第二条跑道 v2，与第一条共享同一 Dataset 卡 | 第二次 run 仍用同一 Dataset |
| 11 | `comparison-table` | 6–10s | 对比时逐条看 item、输出和失败类型，再看聚合结果。不要把两组不同样本硬放在一起比。 | 对照表：item / v1 output / v2 output / 失败类别，示意空值 | 先逐条对照，再看汇总 |
| 12 | `failure-focus` | 6–10s | 平均分看起来变好，也可能藏着关键样本回退。失败样本必须单独展开。 | 平均分卡退到背景，红色失败样本卡放大到前景 | 平均分会掩盖关键样本回退 |
| 13 | `score-attachment` | 6–10s | Score 是附着在运行记录上的评分结果。要知道评分名称、规则、值和它关联的 item 或 run。 | Score 卡连接 item、run 与 evaluator，连线均标示意 | Score 要能追到评分规则和对象 |
| 14 | `run-metadata` | 6–10s | 一次可复核的 run，还要有 Dataset 版本、Prompt、模型、参数、代码版本和运行时间。 | 元数据清单分成六格，版本与 commit 用脱敏占位 | 把这次 run 的条件完整留下 |
| 15 | `trace-link` | 6–10s | 失败样本还要能打开对应 Trace，看输入、输出、错误和中间步骤，而不是只留一个低分。 | 失败 item → run item → Trace 树，低分卡只占一角 | 低分背后要有可回看的 Trace |
| 16 | `readback-loop` | 6–10s | 真正验收时，回读 Dataset、run、Score 和 item 关系，确认它们属于这一轮，而不是历史截图。 | 四步闭环：写入 → 标识 → 回读 → 关系核对 | 回读同一轮的 Dataset、run 和 Score |
| 17 | `boundary-gate` | 6–10s | 没有项目权限或回读失败，就保持 BLOCKED。health 200 和页面打开都不能替代实验成功。 | 红色 BLOCKED 门挡住 health / UI 截图，真实 run 区留白 | health 200 ≠ Dataset run 已完成 |
| 18 | `representativeness` | 6–10s | 固定输入只解决重复比较，不自动保证样本有代表性。三条演示样本更不能代表业务总体。 | 三粒样本点旁是大片未覆盖的业务分布，标「覆盖仍待评估」 | 固定样本 ≠ 样本有代表性 |
| 19 | `stamp` | 6–10s | 本集画面是 prototype、L1 示意，不代表当前实例已完成 Dataset run、Score 写入或实验回读。 | PROTOTYPE / L1 印章，写入、run、Score、回读全部标未证明 | prototype / L1：不是实验已跑通 |
| 20 | `cta` | 6–10s | 下一集讲 Evaluation 和 Score：有了分数，为什么仍然不能直接做上线决定？ | LF-06 预告卡：分数、失败样本、决策门三者并排 | 下一集：有了分数，能否直接上线？ |

## 固定构图顺序

`hook → two-demo → dataset-card → item-grid → id-tag → input-output → freeze-board → run-first → single-variable → run-second → comparison-table → failure-focus → score-attachment → run-metadata → trace-link → readback-loop → boundary-gate → representativeness → stamp → cta`

## 字幕与旁白

- 声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`，禁止整段变速。
- 首次出现中英并读：Dataset 数据集、item 样本、run 一次实验运行、Score 评分。
- 烧录字幕使用表中短句；SRT、VTT 使用同一时间轴，最后一条与片尾对齐。
- 不出现虚构的提升百分比、统计显著、成本节省或模型排名。

## 演示与证据边界

1. 录制时保存 run 标识、Dataset 版本、item 数量、Prompt/模型/参数、commit 和时间。
2. 保存脱敏 item、两次 run、Score、失败样本和同轮回读；缺证据就保持 `BLOCKED`。
3. “可重复”指固定输入和条件的重复比较，不保证模型输出确定，也不证明样本代表性。
4. 当前文件只定义镜头和概念口径，不证明当前实例已写入或回读。
5. 单次 run、单个 Score 或一次平均分不能推出整体稳定、模型更好或统计显著。

## 官方来源（录制当天复核）

- Datasets：https://langfuse.com/docs/datasets
- Experiments：https://langfuse.com/docs/evaluation/experiments
- Observability：https://langfuse.com/docs/observability
