# Langfuse 微课地图：从第一条 Trace 到生产治理

**课程原则**：每集只回答一个问题，控制在约 3 分钟；先展示可运行的最小例子，再解释术语；所有版本、UI 截图和 API 以拍摄当天官方文档为准。官方入口：[Langfuse Docs](https://langfuse.com/docs)。

## 课程路径

| 集数 | 层级 | 标题 | 一句话结果 | 前置 | 演示对象 | 官方依据 |
|---|---|---|---|---|---|---|
| 01 | 入门 | Langfuse 到底记录什么？ | 能说清 Trace、Observation、Score 的关系 | 无 | UI 项目与一条 Trace | [Overview](https://langfuse.com/docs) |
| 02 | 入门 | 5 分钟接入第一条 Trace | 能把一次 LLM 调用送进 Langfuse | 01 | Python SDK 最小脚本 | [Python SDK](https://langfuse.com/docs/sdk/python) |
| 03 | 入门 | Trace、Span、Generation 怎么区分？ | 能按调用树定位一次请求 | 01–02 | 父子 Observation 树 | [Data Model](https://langfuse.com/docs/observability/data-model) |
| 04 | 入门 | 为什么要给 Trace 命名和加元数据？ | 能按用户、会话、版本筛选请求 | 02 | `userId`、`sessionId`、metadata | [Tracing Features](https://langfuse.com/docs/observability/features) |
| 05 | 入门 | 在 UI 里读懂一条 Trace | 能从输入、输出、耗时、token 找到问题 | 03–04 | Trace detail 页面 | [Tracing](https://langfuse.com/docs/observability) |
| 06 | 基础 | Generation 里的模型和 token 怎么看？ | 能解释模型、usage、成本字段 | 03 | Generation + usage | [Models & Costs](https://langfuse.com/docs/observability) |
| 07 | 基础 | 多步骤 Agent 如何画成调用树？ | 能把 LLM、工具、检索步骤串起来 | 03 | Agent/Tool/Generation 树 | [Agent Observability](https://langfuse.com/docs/observability) |
| 08 | 基础 | Prompt 为什么要集中管理？ | 能把 Prompt 从代码中抽出来版本化 | 02 | Prompt 管理页与 SDK 获取 | [Prompt Management](https://langfuse.com/docs/prompt-management) |
| 09 | 基础 | Prompt 版本和标签怎么安全发布？ | 能用 label 区分测试与生产 Prompt | 08 | `production` / `staging` label | [Prompt Versioning](https://langfuse.com/docs/prompt-management) |
| 10 | 基础 | Dataset 是什么？ | 能建立可重复运行的输入样本集 | 05 | Dataset 与 Dataset item | [Datasets](https://langfuse.com/docs/datasets/overview) |
| 11 | 进阶 | 用 Dataset 跑第一次实验 | 能把 Prompt/模型改动放进实验 | 08–10 | Dataset run | [Experiments](https://langfuse.com/docs/datasets/overview#experiments) |
| 12 | 进阶 | Annotation Score 和 Eval Score 有何不同？ | 能区分人工标注、代码评分和模型评分 | 05 | 三种 Score 写入方式 | [Scores](https://langfuse.com/docs/observability/features/scores) |
| 13 | 进阶 | 给 Trace 加一个可复现的评测分数 | 能把评分结果绑定到 Trace | 12 | Score API/SDK | [Score API](https://langfuse.com/docs/evaluation/overview) |
| 14 | 进阶 | LLM-as-a-Judge 怎么避免自说自话？ | 能为 judge 写标准、样例和边界 | 12–13 | evaluator + rubric | [Evaluation](https://langfuse.com/docs/evaluation/overview) |
| 15 | 进阶 | 评测结果如何比较两个 Prompt？ | 能按同一 Dataset 比较版本 | 09–11 | 两次 run 的分组对比 | [Prompt Experiments](https://langfuse.com/docs/prompt-management) |
| 16 | 进阶 | 延迟和 token 成本在哪里看？ | 能找出慢调用和高成本调用 | 06 | latency、input/output tokens、cost | [Tokens & Costs](https://langfuse.com/docs/observability) |
| 17 | 生产 | 用户反馈如何回流评测？ | 能把反馈映射为 Score 或事件 | 12–13 | user feedback → score | [User Feedback](https://langfuse.com/guides/user-feedback-loop) |
| 18 | 生产 | Sampling 怎么控制观测成本？ | 能解释采样对可见性和费用的影响 | 05–06 | SDK/环境采样配置 | [Sampling](https://langfuse.com/docs/observability/features/sampling) |
| 19 | 生产 | 数据保留、脱敏与权限怎么做？ | 能列出上线前的治理检查项 | 05 | masking、retention、RBAC | [Security](https://langfuse.com/docs/administration/data-retention) |
| 20 | 生产 | 从 Trace 到告警：一套排障闭环 | 能把异常发现、定位、修复、回归串起来 | 05–19 | Dashboard + trace + dataset regression | [Dashboards](https://langfuse.com/docs/observability/features/dashboards) |

## 每集固定制作字段

```yaml
id: LF-XX
title: ""
question: ""
one_sentence_result: ""
claim_level: L1|L2|L3
official_sources: []
version_checked_at: "YYYY-MM-DD"
prerequisites: []
demo:
  inputs: []
  steps: []
  expected_observation: ""
  failure_case: ""
assets:
  script: ""
  raw_log: ""
  screenshot: ""
  video: ""
status: planned|scripted|verified|prototype|ready
```

## 证据与版本规则

1. 官方文档只证明“功能如何工作”，不自动证明某个部署实例已经可用；实例演示必须留运行日志或 UI 截图。
2. 每集拍摄前记录 Langfuse 版本、SDK 版本、文档 URL 和核对日期；UI 变动后重新截屏。
3. 出现模型、token、成本或延迟数字时，保存原始输入、输出、参数、时间和项目配置；示意数字必须持续标注“示意”。
4. 自托管相关内容优先引用 [Self-hosting](https://langfuse.com/self-hosting) 与对应版本文档，不把本地部署经验泛化为云端行为。
5. 一集只交付一个动作：打开哪里、运行什么、看哪个字段或做哪项比较。

## 第一轮建议

先制作 LF-01、LF-02、LF-03：它们共同建立 Trace 的最小心智模型。第一轮不急着讲完整评测框架；观众能在本地看到一条有父子关系的 Trace，才进入 Prompt、Dataset 和 Score。
