# Langfuse 微课：Prompt、数据集与 Evaluation（LF-03）

本文件只使用 Langfuse 官方文档描述的能力。具体 UI、SDK 参数和版本在录制前必须按当前部署核对；没有真实运行记录时，画面数字一律标记为“演示”。

## 第 4 集：Prompt 为什么要进入 Langfuse？

**一句话结果**：观众能把一个 Prompt 从代码常量改成可版本化、可观察的 Prompt 资产。

**3 分钟时间轴**

- 0:00–0:15：钩子——“Prompt 改了一行，为什么线上质量突然变了？”
- 0:15–0:45：解释 Prompt 管理、版本和调用记录之间的关系。
- 0:45–1:45：演示：在 Langfuse Prompt 管理界面创建模板，保存版本；在���用侧读取 Prompt 并把渲染后的输入送入一次 Generation。
- 1:45–2:30：展示 Trace 中使用的 prompt/version 字段，说明如何回看变更。
- 2:30–3:00：决策卡——上线前冻结版本，实验时显式记录版本。

**演示步骤**

1. 打开当前 Langfuse 项目的 Prompt 页面，记录实例版本和访问日期。
2. 创建一个带变量的模板，例如 `Answer the question: {{question}}`；保存版本号。
3. 在应用代码中拉取该 Prompt，填入一条脱敏问题并执行一次 Generation。
4. 打开对应 Trace，核对 Prompt 版本、输入、输出和时间戳。

**官方来源**：https://langfuse.com/docs/prompt-management；https://langfuse.com/docs/observability/features/prompts

**边界**：不能据此宣称某个 Prompt 版本质量更好；需要数据集和评分结果。

## 第 5 集：数据集是怎样支持可重复评测的？

**一句话结果**：观众能建立一组带输入和期望结果的数据集，并用同一批样本重复运行实验。

**时间轴**

- 0:00–0:15：同一个 Demo 变好，可能只是换了题。
- 0:15–0:50：解释 Dataset item、输入、期望输出/参考信息和元数据。
- 0:50–1:50：演示创建数据集、加入 3 条脱敏样本、查看 item 列表。
- 1:50–2:35：演示用数据集触发一次实验/评估，并记录运行名称。
- 2:35–3:00：决策卡——固定样本、固定版本、固定评分规则，才有可比性。

**演示步骤**

1. 在 Langfuse Dataset 页面创建 `intro-demo-v1`。
2. 添加三条最小样本，保存 `input` 与可选 `expected_output`；不要上传密钥或个人信息。
3. 用 SDK 或当前支持的运行入口对数据集逐条执行；为每次运行记录 run name。
4. 回看每个 item 关联的 Trace，并核对失败样本没有被过滤。

**官方来源**：https://langfuse.com/docs/datasets；https://langfuse.com/docs/evaluation/experiments

**边界**：三条样本只证明演示流程可运行，不能代表业务总体效果。

## 第 6 集：Evaluation 结果应该怎样读？

**一句话结果**：观众能区分“运行完成”“有分数”和“足以做决策”这三个层次。

**时间轴**

- 0:00–0:15：一个平均分为什么不能替你做上线决定？
- 0:15–0:50：解释 evaluator、score、实验运行和原始 Trace 的关系。
- 0:50–1:40：演示对同一数据集运行一个简单规则评分器，记录每条 item 的分数。
- 1:40–2:30：把总分、分组分数和失败样本并排展示。
- 2:30–3:00：决策卡——先看样本和失败，再看聚合分数。

**演示步骤**

1. 从上一集数据集选取三条样本，固定 Prompt 版本和模型参数。
2. 定义一个可解释的评分规则（例如是否包含必需字段），保存评分方法文本。
3. 运行实验，记录每条 item 的 score、运行时间和原始输出。
4. 将聚合结果与失败样本一起截图/导出；不要只保存排行榜数字。

**官方来源**：https://langfuse.com/docs/evaluation/overview；https://langfuse.com/docs/evaluation/evaluation-methods；https://langfuse.com/docs/evaluation/experiments

**边界**：规则评分器不是通用质量判断；LLM-as-a-judge 也需要校准、抽样复核和失败分析。

## 发布前统一核验

- [ ] URL 在录制当天可访问，并记录检索日期。
- [ ] Langfuse 版本、SDK 版本和部署方式写入片尾或仓库元数据。
- [ ] 所有输入已脱敏；不在视频中出现密钥、用户数据或内部 Prompt。
- [ ] 每个分数可回指 dataset item、Trace、评分方法和运行时间。
- [ ] 示例数字明确标注“演示”；没有真实结果就不说“提升”“领先”或“最佳”。
