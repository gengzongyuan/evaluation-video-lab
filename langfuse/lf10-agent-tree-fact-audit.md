# LF-10 事实审计：多步骤 Agent 调用树

任务：LF10-S1。官方文档核对日期：2026-11-23（Asia/Shanghai）；本集为概念课程，当前无项目 key，未执行真实运行。

## 结论

这集要守住一句话：**把 Agent、检索、工具和模型调用放进一棵可解释的 Trace tree，知道哪里需要回读验证。一棵完整的树帮助排障，不自动证明任务质量、工具安全或所有分支都被采样。**

- 最外层 Trace 关联一次请求；普通步骤是 span，模型调用是 generation，工具调用是 tool，agent 是决定流程的工作单元。
- 父子关系跟真实调度；UI 和 API 对照检查孤立、重复、错挂节点。状态保持 `prototype / L1`。

## 官方类型与字段（2026-11-23 读取）

来源：<https://langfuse.com/docs/observability/features/observation-types>、<https://langfuse.com/docs/observability/data-model>

| 类型 | 官方定义 |
|---|---|
| `agent` | 决定应用流程，可在 LLM 指导下使用工具 |
| `tool` | 工具调用 |
| `generation` | 模型调用，含 prompt、token usage、cost |
| `span` | 普通处理步骤（检索、解析等） |

节点校验字段：`type`、`name`、`parentObservationId`、`input`、`output`、`status`。具体字段名以录制当天 API/UI 为准。

## 与现有 LF-10 审计的对齐

`lf10-fact-audit.md` 已覆盖可讲范围、不可证明范围、最小证据包。本文件补上官方 observation-types 的 agent/tool/generation/span 定义。旧文件里“以及”有乱码，建议后续修正。

## 与其他 agent 的冲突

- 若有人把示意调用树当成当前实例新 Trace，与本审计冲突。
- 若有人把一条完整树当成任务质量/工具安全/全部分支已采样，与本审计冲突。
- 若有人用历史 Trace、health、OTEL 认证门替代本轮同一 Trace ID 写入与回读，与本审计冲突。

## 需要冻结的字段

- 状态：`prototype / L1`；真实 Agent/Tool/Generation 写入与回读 `BLOCKED`。
- 主线类型：agent / tool / generation / span。
- 节点校验：type、name、parentObservationId、input、output、status。
- 禁出现：内网地址、真实 key / secret、Authorization 值、登录信息、PII。

## 依据

官方页面，2026-11-23 以 Markdown 端点读取：

- Observation 类型：<https://langfuse.com/docs/observability/features/observation-types>
- 数据模型：<https://langfuse.com/docs/observability/data-model>

仓库内证据：

- `langfuse/lf10-fact-audit.md`
- `langfuse/lf10-agent-observability-lesson.md`
- `langfuse/lf03-observation-types-fact-audit.md`

## 产物与验证

独占产物：本文件。未改视频、字幕、播放器、manifest 或 `docs/quality/00-project-state.md`，未 git commit。

## 风险、缺口与未完成

- 没有项目 key，真实调用树写入、UI/API 回读、字段一致性全部未验证。
- 完整树不等于任务质量或工具安全。

## 建议下一步

由主 agent 把 LF-10 口播对齐官方 observation-types。等级升级只能等受保护写入与同一 Trace ID 回读证据。
