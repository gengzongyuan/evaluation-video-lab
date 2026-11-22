# LF-04 事实审计：Prompt 管理、版本和 label

任务：LF04-S1。官方文档核对日期：2026-11-23（Asia/Shanghai）；本集为概念课程，当前无项目 key，未执行真实运行。

## 结论

这集要守住一句话：**把 Prompt 集中管理，用版本和 label 让一次运行可追溯；先记录版本，再谈效果。label 存在不等于效果更好。**

- Prompt 集中管理，应用侧按需获取；版本号自动分配，label 用来指向环境/租户/实验。
- 把 Prompt 链接到 Trace，才能按版本看指标和评估。
- 官方文档证明功能和字段语义，不证明当前项目权限、UI 布局或某版本已发布。状态保持 `prototype / L1`。

## 官方能力与字段（2026-11-23 读取）

来源：<https://langfuse.com/docs/prompt-management/features/prompt-version-control>、<https://langfuse.com/docs/prompt-management/overview>、<https://langfuse.com/docs/prompt-management/features/link-to-traces>

| 概念 | 官方口径 | 不能推出 |
|---|---|---|
| 版本 | 每个 prompt version 自动分配 version ID | 某版本已发布到生产 |
| label | 自定义标签，指向环境（staging/production）、租户（tenant-1/2）或实验（prod-a/b） | label 存在就等于效果更好 |
| 推广/回退 | UI 可把 production label 移到新版本，也可退回旧版本 | 当前实例已完成推广 |
| 集中管理 | 非工程成员在 UI 改 prompt，应用自动取最新；SDK 客户端缓存，低延迟 | 改 prompt 零风险 |
| 链接 Trace | 把 prompt 链到 trace，按版本看 latency、cost、scores | 当前实例已链接并产生指标 |

## 链接 Trace 的意义

把 prompt 链到 generation observation 后，Langfuse 会按 prompt 版本聚合 latency、cost、scores。这样才能回答“这次回答用的是哪一版 prompt”，并按版本比较。`propagate_attributes(prompt=...)` 可让同一上下文里多个 generation 用同一版本。

## 最小证据包

要把“演示目标”升级成“本轮观察到”，至少需要：

1. 页面 URL、核对日期、Web/SDK 版本、字段截图。
2. 不含密钥/PII 的 Prompt，v1/v2 内容摘要、版本号、label、创建时间。
3. 应用侧按 label/版本获取 Prompt 的脱敏请求、响应和实际返回版本。
4. 同一请求的 Trace ID、Prompt 版本/label metadata 与 UI/API 回读配对。
5. 若出现 401/404/字段不一致，保留原始响应并标记 `needs-review` 或 `BLOCKED`。

## 与现有 LF-04 课稿/审计的对齐

`lf04-prompt-lesson.md` 与 `lf04-fact-audit.md` 的方向一致：版本、label、应用侧获取、追溯。需要修正的一点：旧审计引用了 `/docs/sdk/python`，该路径已过时；当前应指向 SDK 概览与 prompt-management 的 version-control / link-to-traces 页面。

## 与其他 agent 的冲突

- 若有人把“创建 v1/v2、绑定 label”说成当前实例已发生，与本审计冲突；那是演示步骤。
- 若有人用“更好/更快/节省”作结论而没有同条件证据，与本审计冲突。
- 若有人沿用旧 `/docs/sdk/python` 作来源，以本文件的当前路径为准。

## 需要冻结的字段

- 状态：`prototype / L1`；真实实例写入/获取/回读 `BLOCKED`。
- 版本自动分配；label 指向环境/租户/实验；label 可回退。
- 链接 Trace 后才能按版本看 latency/cost/scores。
- 禁出现：内网地址、真实 key / secret、Authorization 值、登录信息、PII。

## 依据

官方页面，2026-11-23 以 Markdown 端点读取：

- Version Control：<https://langfuse.com/docs/prompt-management/features/prompt-version-control>
- 概览：<https://langfuse.com/docs/prompt-management/overview>
- Link to Traces：<https://langfuse.com/docs/prompt-management/features/link-to-traces>

仓库内证据：

- `langfuse/lf04-prompt-lesson.md`
- `langfuse/lf04-fact-audit.md`
- `langfuse/lf14-version-pinning-fact-audit.md`

## 产物与验证

独占产物：本文件。未改视频、字幕、播放器、manifest 或 `docs/quality/00-project-state.md`，未 git commit。

## 风险、缺口与未完成

- 没有项目 key，真实 Prompt 创建、label 解析、Trace 回读全部未验证。
- 具体字段和 UI/API 行为需在录制当天按当前官方页面核对。

## 建议下一步

由主 agent 把 LF-04 口播对齐 version-control 与 link-to-traces，替换过时 SDK 路径。等级升级只能等受保护 Prompt 创建、获取与同一 Trace 回读证据。
