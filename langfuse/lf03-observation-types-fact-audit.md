# LF-03 事实审计：Span、Generation、Tool、Agent

任务：LF03-S1。官方文档核对日期：2026-11-23（Asia/Shanghai）；本集为概念课程，当前无项目 key，未执行真实运行。

## 结论

这集要守住一句话：**按“这一步到底做了什么”选 Observation 类型，用父子关系解释调用树；类型对，才能知道这一步发生了什么。有记录不等于回答正确，health 正常也不等于新 Trace 已写入。**

- Langfuse 把 span 统称为 observation；`span` 本身也是一种具体的 observation 类型。
- 模型调用是 `generation`，检索/解析等普通步骤是 `span`，工具调用是 `tool`，决定流程的工作单元是 `agent`。
- 父子关系跟着真实调度走，不要为了 UI 好看伪造层级。
- 状态保持 `prototype / L1`；真实调用树未在当前实例验证。

## 官方 Observation 类型（2026-11-23 读取）

来源：<https://langfuse.com/docs/observability/features/observation-types>

| 类型 | 官方定义 | 关键观察 | 不能推出 |
|---|---|---|---|
| `event` | 基本构建块，追踪 trace 里的离散事件 | 时间点 | 步骤耗时 |
| `span` | 普通处理步骤（检索、解析、路由等） | 开始/结束、输入输出、父节点 | 模型质量分 |
| `generation` | AI 模型的生成，含 prompt、token usage、cost | model、input/output、usage、延迟 | 有记录就等于回答正确 |
| `agent` | 决定应用流程，可在 LLM 指导下使用工具 | 调度边界、子步骤、状态 | 全链路已可观测 |
| `tool` | 工具调用 | 工具名、参数、结果、错误 | 工具一定安全 |
| `chain` | 应用步骤之间的链接，如把 retriever 的上下文传给 LLM | 步骤衔接 | — |
| `retriever` | 检索 | 检索输入输出 | — |
| `evaluator` | 评估器 | 评估过程 | — |
| `embedding` | 调用 LLM 生成 embedding，含 model、token、cost | 向量生成 | — |
| `guardrail` | 护栏 | 拦截/放行 | — |

集成框架会自动设置类型，例如 LangChain 里 `@tool` 会把 observation 标成 `tool`；SDK 里可用 `as_type` / `asType` 指定。

## 父子关系与验收

先画真实调用顺序，再决定父子关系。验收不要只看 UI：记下 Trace ID，按 ID 回读 `type`、`name`、`parentObservationId`、input/output 和 usage；没有 usage 就写 `unknown`。类型错挂、重复记录、输入输出泄露或回读的不是本次运行，都算 FAIL。

## 与现有 LF-03 课稿的对齐

`lf03-type-card.md`、`lf03-script-revision.md`、`lf03-demo-plan.md` 的方向与本审计一致：Span/Generation/Tool/Agent 分类、父子关系、UI+API 回读、当前 BLOCKED。需要保留的收紧点：

- 讲清“span 是统称 observation，也是具体类型”这层，避免观众混淆。
- 类型卡可补上 chain/retriever/embedding/guardrail 的提及，但主线仍是 Span/Generation/Tool/Agent。
- 历史实验里出现过 AGENT 根节点和 GENERATION 节点，不替代当前版本重跑。

## 与其他 agent 的冲突

- 若有人把 health 200 或历史调用树当成当前实例新 Trace 已跑通，与本审计冲突。
- 若有人为 UI 美观伪造父子层级，与“父子关系跟真实调度”冲突。
- 若有人把 generation 有记录当成回答正确，与类型定义冲突。

## 需要冻结的字段

- 状态：`prototype / L1`；真实调用树 `BLOCKED`。
- 主线类型：span / generation / tool / agent。
- 回读字段：type、name、parentObservationId、input/output、usage。
- 禁出现：内网地址、真实 key / secret、Authorization 值、登录信息、PII。

## 依据

官方页面，2026-11-23 以 Markdown 端点读取：

- Observation 类型：<https://langfuse.com/docs/observability/features/observation-types>
- 数据模型：<https://langfuse.com/docs/observability/data-model>

仓库内证据：

- `langfuse/lf03-type-card.md`
- `langfuse/lf03-script-revision.md`
- `langfuse/lf03-demo-plan.md`

## 产物与验证

独占产物：本文件。未改视频、字幕、播放器、manifest 或 `docs/quality/00-project-state.md`，未 git commit。

## 风险、缺口与未完成

- 没有项目 key，真实调用树、类型回读、usage 全部未验证。
- 历史 AGENT/GENERATION 结构不替代当前版本重跑。

## 建议下一步

由主 agent 把 LF-03 口播补上“span 是统称也是具体类型”的区分。等级升级只能等受保护写入与同一 Trace ID 的类型/父子关系回读证据。
