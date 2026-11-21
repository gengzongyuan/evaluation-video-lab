# LF-04 事实与来源审计

日期：2026-11-22（Asia/Shanghai）

## 结论

LF-04 可以制作成 `prototype / L1` 快切课程：官方页面可作为 Prompt Management 的功能和术语来源，脚本可讲“版本、label、应用侧获取和追溯”的方法。当前没有项目 key、当前 UI 录屏或本轮 API 回读，因此不能把脚本示意说成当前实例已创建 v1/v2、label 已生效或请求已回指某个版本。

## 来源核验

| 来源 | HTTP | 可支持 | 不能支持 |
|---|---:|---|---|
| https://langfuse.com/docs/prompt-management | 200 | Prompt 管理入口、版本与 label 概念，录制前需核对当前字段和示例 | 当前项目权限、当前 UI 布局、当前实例版本是否已发布该字段 |
| https://langfuse.com/docs/observability/features | 200 | 作为可观测功能导航和字段方向 | 某次 Prompt 请求已经生成 Trace 或效果提升 |
| https://langfuse.com/docs/sdk/python | 200 | SDK 接入方向和录制前 API 复核入口 | 当前 shell 凭据、网络、项目权限或本地运行成功 |

## 脚本断言风险

- “保存 Prompt、版本、标签，并从应用侧获取”是官方能力方向；录制时必须按当前页面确认具体 SDK/API 字段。
- “创建 v1、修改成 v2、绑定测试/生产 label”目前是演示步骤，不是已发生的本地运行事实。
- “输出可回指 Prompt 版本”只有在同一轮取得响应、请求版本/label、Trace metadata 和回读结果后才能说“本轮观察到”；否则应说“演示目标”。
- “先记录版本，再谈效果”是流程建议，不是质量提升结论。
- 任何“更好、更快、节省”都必须有同条件 Dataset、模型、参数和评分证据；当前课程不应使用这些词作结论。

## 录制前最小证据包

1. 保存页面 URL、核对日期、Langfuse Web/SDK 版本和当前字段截图。
2. 使用不含密钥和 PII 的 Prompt，记录 v1/v2 内容摘要、版本号、label、创建时间。
3. 从应用侧按 label/版本获取 Prompt，保存脱敏请求、响应和实际返回版本。
4. 将同一请求的 Trace ID、Prompt 版本/label metadata 与 UI/API 回读配对。
5. 若发生 401/404/字段不一致，保留原始响应并将课程标记为 `needs-review` 或 `BLOCKED`。
6. 不把官方能力、历史截图、health/readiness 或空请求认证探针混成 Prompt 已发布事实。

## 当前发布判定

- 媒体：等待 LF-04 v2 质量门。
- 内容事实：`needs-review`，因为具体字段和 UI/API 行为要在录制当天按当前官方页面核对。
- 真实实例：`BLOCKED`，当前无项目 key 和本轮 Prompt 写入/获取/回读证据。
- 证据等级：保持 `prototype / L1`。

## 验证

- `curl -L -s -o /dev/null -w '%{http_code}\\n'` 对三个来源均返回 `200`。
- `test -s langfuse/lf04-prompt-lesson.md` 和 `test -s langfuse/demo-experiments.md` 通过。
