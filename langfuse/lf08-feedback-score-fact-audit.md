# LF-08 事实审计：用户反馈回流 Score

任务：LF08-S1。官方文档核对日期：2026-11-23（Asia/Shanghai）；本集为概念课程，当前无项目 key，未执行真实运行。

## 结论

这集要守住一句话：**把用户反馈和原始 Trace 对上，再写成可解释的 Score。单条反馈不能推出总体满意度。**

- 在 Langfuse 里，反馈被捕获为 score 并链接到 trace。
- 反馈分显式（点赞/点踩、星级、评论）和隐式（行为信号）。
- 当前无项目 key，反馈写入、回读、满意度分析全部 BLOCKED。状态保持 `prototype / L1`。

## 官方反馈机制（2026-11-23 读取）

来源：<https://langfuse.com/docs/observability/features/user-feedback>

| 项 | 官方口径 | 边界 |
|---|---|---|
| 载体 | 反馈捕获为 score，链接到 trace | 单条反馈不代表总体满意度 |
| 显式反馈 | 点赞/点踩、星级、评论 | 需关联 trace ID |
| 隐式反馈 | 行为信号 | 需说明采集口径 |
| 用途 | 按 score 过滤 trace、建 annotation queue、作自动化评估的 ground truth | 不等于已建立评估 |
| 实现 | 后端把 trace ID 返回前端，前端据此把反馈链到 trace | 需同一 ID 回读 |

反馈作为 score，沿用 Score 数据模型：source 为 API/EVAL/ANNOTATION，类型 numeric/categorical/boolean/text。

## 与现有 LF-08 审计的对齐

`lf08-fact-audit.md` 已覆盖来源、断言风险、最小证据包。本文件补上官方“反馈=score 链到 trace”“显式/隐式两类”“trace ID 回前端”的具体机制。旧文件里“反馈”有乱码，且引用了 `/docs/observability/features/scores`，建议修正为 `/docs/evaluation/scores/...`。

## 与其他 agent 的冲突

- 若有人把单条正负反馈说成总体满意/不满意，与本审计冲突。
- 若有人把健康检查、空请求认证响应当成反馈已回流，与本审计冲突。
- 若有人沿用旧 `/docs/observability/features/scores` 作来源，以本文件为准。

## 需要冻结的字段

- 状态：`prototype / L1`；反馈写入/回读/满意度 `BLOCKED`。
- 反馈=score 链到 trace；显式/隐式两类。
- 禁出现：内网地址、真实 key / secret、Authorization 值、登录信息、PII、未脱敏反馈原文。

## 依据

官方页面，2026-11-23 以 Markdown 端点读取：

- User Feedback：<https://langfuse.com/docs/observability/features/user-feedback>
- Scores 数据模型：<https://langfuse.com/docs/evaluation/scores/data-model>

仓库内证据：

- `langfuse/lf08-fact-audit.md`
- `langfuse/lf08-feedback-lesson.md`

## 产物与验证

独占产物：本文件。未改视频、字幕、播放器、manifest 或 `docs/quality/00-project-state.md`，未 git commit。

## 风险、缺口与未完成

- 没有项目 key，真实反馈写入、回读、满意度分析全部未验证。
- 反馈原文必须脱敏。

## 建议下一步

由主 agent 把 LF-08 口播补上“反馈=score 链到 trace”和显式/隐式两类。等级升级只能等受保护写入与同一 trace ID 回读证据。
