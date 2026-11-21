# LF-08｜用户反馈如何回流 Score

## 一句话结果
看完后，观众能把用户反馈和原始 Trace 对上，再写成可解释的 Score 或事件。

## 演示步骤

1. 选择一条脱敏 Trace，记录 trace_id 和用户反馈上下文。
2. 定义反馈类型、取值范围、来源和时间；不要把没有标签的评论直接当分数。
3. 按当前官方 SDK/API 把反馈绑定到 Trace 或 Observation。
4. 回读 Score 与原始输入输出，抽查正例、负例和空值。
5. 把反馈样本放回 Dataset，作为下一轮回归或人工复核素材。

## 证据边界

反馈回流能建立数据闭环，不自动代表真实用户总体满意度；必须保留采样方式、缺失反馈和隐私处理。当前项目 Key 缺失，正式写入/回读保持 BLOCKED。

来源：<https://langfuse.com/docs/evaluation/evaluation-methods/user-feedback>、<https://langfuse.com/docs/observability/features/scores>。
