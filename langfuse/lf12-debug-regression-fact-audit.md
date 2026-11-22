# LF-12 事实审计：异常 Trace 到修复和回归

任务：LF12-S1。官方文档核对日期：2026-11-23（Asia/Shanghai）；本集为概念课程，当前无项目 key，未执行真实运行。

## 结论

这集要守住一句话：**把异常发现、Trace 定位、修复、回归和告警串成闭环。一张漂亮的 Dashboard 截图不能替代闭环证据。**

- 监控信号是调查入口，不是根因；定位到具体 Trace 再分类失败。
- 修复记录 commit，用固定 Dataset 回归重跑，保留修复前后失败样本。
- 没有原始 Trace、失败样本和回归证据，只能 needs-review/blocked。状态保持 `prototype / L1`。

## 闭环与边界

闭环：signal → Trace → root cause → commit → regression → alert/rollback。

- Dashboard 帮助发现异常，不能替代原始 Trace、失败样本或修复后回归回读。
- 单次成功运行、历史 Trace、health/readiness 不能证明修复有效、错误率下降或没有回归。
- 没有多样本回归和同条件对照，不能声称问题已解决。

## 与现有 LF-12 审计的对齐

`lf12-fact-audit.md` 已覆盖可讲范围、不可证明范围、最小证据包、发布门。本文件强调闭环顺序和“Dashboard≠闭环证据”。

## 与其他 agent 的冲突

- 若有人用虚构错误率/延迟/回归分数或“已修复”结论，与本审计冲突。
- 若有人用一张 Dashboard 截图替代闭环证据，与本审计冲突。

## 需要冻结的字段

- 状态：`prototype / L1`；异常 Trace、修复、回归、告警闭环 `BLOCKED`。
- 闭环：signal→Trace→root cause→commit→regression→alert/rollback。
- 禁出现：内网地址、真实 key / secret、Authorization 值、登录信息、PII。

## 依据

- Dashboards：<https://langfuse.com/docs/observability/features/dashboards>
- Experiments：<https://langfuse.com/docs/evaluation/experiments>

仓库内证据：`langfuse/lf12-fact-audit.md`、`langfuse/lf12-debugging-loop-lesson.md`。

## 产物与验证

独占产物：本文件。未改视频、字幕、播放器、manifest 或 `docs/quality/00-project-state.md`，未 git commit。

## 风险与下一步

没有项目 key，真实异常/修复/回归未验证。由主 agent 保持闭环口径，示意画面固定标 prototype/L1。
