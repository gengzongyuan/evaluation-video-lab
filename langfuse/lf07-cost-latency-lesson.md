# LF-07｜Generation 的模型、usage、延迟和成本

## 一句话结果
看完后，观众能在一次 Generation 里找到模型、token usage、耗时和成本字段，并知道缺字段时不能猜。

## 3 分钟结构

- 0–20s：一次回答很慢，先别说“模型慢”，先拆开等待时间和模型调用时间。
- 20–70s：展示 Generation 的 model、input/output、usage、start/end/latency。
- 70–125s：用同一输入跑两个条件，保存原始字段；比较时固定模型、参数、网络和样本。
- 125–160s：解释成本依赖 provider、价格配置和 usage 完整性；缺失字段写 unknown。
- 160–180s：决策卡：先看原始字段，再谈成本优化。

## 证据边界

官方文档说明字段和配置方式；一次本地 Trace 不能推出长期平均延迟、成本或模型整体效率。当前实例没有安全项目 Key，正式回读保持 BLOCKED。

来源：<https://langfuse.com/docs/observability>、<https://langfuse.com/docs/observability/data-model>。
