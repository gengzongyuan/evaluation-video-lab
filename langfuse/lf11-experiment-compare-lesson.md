# LF-11｜用同一 Dataset 比较两个 Prompt/模型

## 一句话结果
看完后，观众能把 Prompt v1/v2 放在同一 Dataset、同一评分规则下比较，并保留失败样本。

## 对比流程

- 冻结 Dataset、模型/参数、评分规则和运行日期。
- 分别执行两个 run，保存 run ID、版本、原始输出、分组分数、失败类型、延迟和成本（缺失写 unknown）。
- 先看每个样本，再看汇总；检查差异是否超过抽样和运行波动。
- 把结论限定在这组数据与条件，不说“全面领先”。

## 边界

实验框架能提高可重复性，不自动解决 Dataset 偏差、评分者偏差或统计显著性。当前没有项目 Key，正式 run/回读保持 BLOCKED。

来源：<https://langfuse.com/docs/evaluation/experiments>、<https://langfuse.com/docs/prompt-management/features/prompt-experiments>。
