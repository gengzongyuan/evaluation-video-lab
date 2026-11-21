# LF-06｜Evaluation、Score 与失败样本

## 一句话结果
看完后，观众能把人工、代码或模型评分绑定到运行证据，并保留失败样本供复核。

## 演示步骤

1. 先定义评分问题、范围、单位和空值规则；不要先写“好/坏”。
2. 用固定 Trace 或 Dataset run 作为被评对象。
3. 写入一个可追溯 Score，记录 evaluator 版本、规则和运行时间。
4. 回读 Score 与原始输入输出，抽查高分和低分样本。
5. 把评分结果用于比较或回归时，保留样本量、失败类型和版本。

## 3 分钟结构

先展示“总分 90”如何掩盖关键失败，再展示 Score + 原始样本 + 规则三件套。结尾强调：Score 是判断工具，不是脱离任务的真理。

## 证据边界

Score API/SDK 的具体参数按当前官方文档核对；没有真实写入和回读，不能声称评分成功。当前项目 Key 缺失，正式评分演示保持 BLOCKED。

来源：<https://langfuse.com/docs/evaluation/overview>、<https://langfuse.com/docs/observability/features/scores>、<https://langfuse.com/docs/api/scores>。
