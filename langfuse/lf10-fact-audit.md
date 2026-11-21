# LF-10 Agent / Tool / Generation 事实与来源审计

## 审计结论

LF-10 可以讲一棵多步骤调用树如何帮助定位问题：最外层 Trace 关联一次请求，普通步骤承载检索或解析，Generation 表示模型调用，Tool 表示外部能力调用（具体类型和字段必须按录制当天的官方 SDK 文档复核）。这些是数据模型和观测方法的课程内容，当前不构成实例已经写入或回读成功的证明。

## 可安全讲述的范围

| 主题 | 可讲范围 | 录制前需复核 |
|---|---|---|
| Trace tree | 用父子关系组织 Agent、检索、工具和模型步骤 | 当前 SDK 如何创建/结束父子 Observation，以��� UI/API 当前回读路径 |
| Agent | 将一个会规划并执行多个步骤的应用流程作为观测单元 | 官方当前是否有专门类型或建议使用的通用 Observation 类型 |
| Tool | 记录访问外部能力的动作、输入输出和状态 | 当前 SDK 支持的类型名、字段名和父级绑定方式 |
| Generation | 记录模型调用、输入输出、模型、usage 和延迟 | 当前 Generation schema、usage 字段和 provider 返回范围 |
| 节点校验 | 检查 `type/name/parentObservationId/input/output/status` 是否一致 | 字段是否仍是当前 API/UI 的准确名称；敏感内容必须脱敏 |

## 不可由现有材料证明的范围

- 示意调用树不等于当前 Langfuse 实例的新 Trace。
- 文档页面 HTTP 200 只能证明页面可访问，不能证明项目权限、SDK 版本或字段在当前实例可用。
- 一条完整树不能证明任务质量、工具安全、所有分支都被采样或 Agent 决策正确。
- 历史 Trace、健康检查、OTEL 认证门和旧 API 迁移提示不能替代本轮同一 Trace ID 的写入与回读。
- 当前 shell 没有受保护项目 key，因此真实 Agent/Tool/Generation 写入、UI/API 回读和字段一致性保持 `BLOCKED`。

## 最小证据包

在允许把示意升级为运行观察前，需要同一轮保存：

1. 脱敏用户问题和运行 metadata（实例、SDK、commit、时间）。
2. 受保护运行的写入响应和关联 Trace ID；不记录 key、secret 或 Authorization。
3. 当前 v4 支持的 UI/API 回读 JSON，核对节点类型、名称、父子关系、状态、错误和时间戳。
4. Tool/Generation 的输入输出脱敏摘要，以及失败分支或孤立节点检查结果。
5. 原始证据 SHA-256 清单和逐条 claim review。

## 来源与门禁

- `https://langfuse.com/docs/observability`
- `https://langfuse.com/docs/observability/data-model`
- `langfuse/evidence-pack-lf06-10.md`
- `langfuse/source-verification.md`

录制当天必须重新打开官方页面并记录日期、页面标题和 SDK/实例版本。若类型名、父子字段或回读路径变化，脚本降为 `needs-review`。本集保持 `prototype / L1`；真实写入与回读缺失时不得标为 verified。

## 验证

```bash
test -s langfuse/lf10-fact-audit.md
rg -n "BLOCKED|prototype / L1|parentObservationId|Trace ID|observability/data-model" langfuse/lf10-fact-audit.md
```
