# LF-03 类型卡：Span、Generation、Tool、Agent

## 一句话结果
看完后，观众能按“这一步到底做了什么”选择更具体的 Observation 类型，并用父子关系解释一次调用树。

| 类型 | 适合描述 | 关��观察 | 不应推出 |
|---|---|---|---|
| Span | 普通处理步骤，如检索、解析、路由 | 开始/结束时间、输入输出、父节点 | 不是模型质量分 |
| Generation | 一次模型调用 | model、input/output、usage、延迟 | 有记录不等于回答正确 |
| Tool | 工具调用（若当前接入方式支持该语义） | 工具名、参数、结果、错误 | 不代表工具一定安全 |
| Agent | Agent 工作单元（若当前版本/SDK支持） | 调度边界、子步骤、状态 | 不代表全链路可观测完整 |

## 父子关系

先画真实调用顺序，再决定父子关系。模型调用是 Generation，检索或解析是 Span；不要为了让 UI 看起来漂亮而伪造层级。应使用当前 SDK 与实例支持的字段名，并在 API 回读中核对 `type`、`name`、`parentObservationId`、输入输出和错误状态。

## 证据边界

官方数据模型只能证明概念和字段语义；当前实例 health 正常不能证明新 Trace 已写入。当前项目没有安全可用的项目 Secret，本集正式实例演示保持 BLOCKED。历史实验中出现过 `AGENT` 根节点和 `GENERATION` 节点，但不替代当前版本重跑。

官方来源：<https://langfuse.com/docs/observability/data-model>、<https://langfuse.com/docs/observability/best-practices>
