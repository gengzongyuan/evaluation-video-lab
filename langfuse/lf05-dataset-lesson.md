# LF-05｜Dataset 与可重复实验

## 一句话结果
看完后，观众能用一组固定输入重复比较 Prompt 或模型，而不是只拿一条示例下结论。

## 最小实验

1. 创建一个只含脱敏输入和期望字段的 Dataset。
2. 为每条 item 保留稳定 ID；记录创建日期、来源和版本。
3. 用 Prompt v1 跑一遍，保存 run 标识、原始输出和评分。
4. 只修改一个变量，再用同一 Dataset 跑 Prompt v2。
5. 对比分组结果、失败样本、运行参数和成本/延迟字段；不能只看平均分。

## 3 分钟结构

钩子是“一条漂亮样例不等于可重复结论”；中段展示 Dataset item → run → result；结尾提醒：实验结果只适用于本次数据、版本和条件。

## 证据边界

Dataset 能支持可重复输入，不自动保证样本代表性；一次 run 不自动证明模型更好。当前实例缺少安全项目 Key，正式 Dataset run 保持 BLOCKED。

来源：<https://langfuse.com/docs/datasets>、<https://langfuse.com/docs/evaluation/experiments>。
