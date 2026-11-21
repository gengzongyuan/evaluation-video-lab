# Langfuse 微课：成本、延迟与生产监控（LF-04）

## 第 7 集：一次调用到底花了多少钱？

**一句话结果**：观众能从一次 Generation 的 usage、模型单价和调用次数估算成本，并知道估算边界。

**3 分钟结构**：0:00 展示“同样回答，成本不同”；0:15 解释 token usage 与价格表是两个来源；0:45 打开 Trace/Generation 的 usage 字段；1:20 用脱敏示例计算输入 token、输出 token、单价和单次成本；2:20 说明批量调用、缓存、重试和价格变更会影响总账；2:45 给出成本记录卡。

**演示步骤**：固定模型和日期；执行一次调用；记录 input/output token、currency、模型名、时间戳；把价格来源 URL 与检索日期写入旁白卡；用公式 `input_tokens × input_price + output_tokens × output_price` 计算示例成本。

**官方来源**：https://langfuse.com/docs/observability/features/token-and-cost-tracking

**边界**：若 usage 未被 SDK/模型提供商返回，不可假设成本准确；价格必须注明检索日期，不把示意价格说成当前报价。

## 第 8 集：延迟慢在哪里？

**一句话结果**：观众能用 Trace 时间线区分总延迟、模型 Generation 延迟和工具/检索 Span 延迟。

**时间轴**：钩子“用户只说慢，但哪一段慢？”；展示 Trace waterfall；逐层定位 LLM、检索和工具调用；比较两次运行的时间字段；给出“先定位再优化”的动作卡。

**演示步骤**：执行一次包含检索或工具调用的流程；打开 Trace timeline；记录 observation start/end、Generation latency 与子 Span；选择一次慢样本和一次基线样本并排查看；不得用单次延迟宣称系统性能改善。

**官方来源**：https://langfuse.com/docs/observability/features/latency-and-performance

**边界**：客户端网络、队列、冷启动和服务端计时口径可能不同；先写清测量点和环境。

## 第 9 集：生产监控不是只看错误数

**一句话结果**：观众能建立由质量分数、成本、延迟、错误和样本 Trace 组成的最小监控面板。

**演示步骤**：选定一个生产时间窗口；按 release/environment/user group 分组；展示 traces、scores、latency、token/cost 和 error 事件；点击一个异常分组回到原始 Trace；把阈值、负责人和处理动作记录在监控说明中。

**官方来源**：https://langfuse.com/docs/observability/overview；https://langfuse.com/docs/observability/features/sessions；https://langfuse.com/docs/observability/features/scores

**边界**：监控图表只说明观测到的窗口；阈值需要业务基线，不能凭示意数据直接报警或回滚。

## 录制前核验

- [ ] Langfuse 与 SDK 版本、部署方式、环境名已记录。
- [ ] Token、成本、延迟字段来自真实 Trace；缺字段则明确“未采集”。
- [ ] 价格来源和检索日期写入证据卡；不出现密钥和个人信息。
- [ ] 监控图表可点击回到样本 Trace；聚合结论保留样本数与时间窗口。
