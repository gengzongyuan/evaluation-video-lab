# Langfuse 来源链接审计（2026-11-22）

## 结论

课程原先引用的一些深链接在当前站点返回 404。已将脚本和课程地图中的这些链接降级到可访问的官方父页或当前 guides/docs 入口，避免发布时给观众死链。具体 API 字段和 UI 仍必须在拍摄当天按官方当前页面核对。

## 修复映射

| 旧路径 | 当前引用 | 处理理由 |
|---|---|---|
| `/docs/api/scores` | `/docs/evaluation/overview` | 保留 Evaluation 概念入口，API 参数录制时再核对 |
| `/docs/evaluation/evaluation-methods/user-feedback` | `/guides/user-feedback-loop` | 使用当前指南入口 |
| `/docs/observability/features/agent-observability` | `/docs/observability` | 使用可访问的 Observability 总入口 |
| `/docs/observability/features/tokens-costs` | `/docs/observability` | 字段和价格配置需按当前页面复核 |
| `/docs/prompt-management/features/prompt-experiments`、`version-control` | `/docs/prompt-management` | 版本/实验细节随文档结构变化，录制时展开当前页面 |
| `/docs/security-and-privacy` | `/docs/administration/data-retention` | 治理主题先落到当前管理文档，权限另行核对 |

## 放行规则

链接返回 200 只证明页面可访问，不证明脚本中的字段、API 参数或当前实例行为。每条视频仍需保存页面标题、核对日期、版本和运行证据；如果页面结构再次变化，状态降回 `needs-review`。
