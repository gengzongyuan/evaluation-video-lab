# LF-12 事实与来源审计：异常 Trace 到修复和回归

核对范围：`lf12-debugging-loop-lesson.md`、`evidence-pack-lf11-15.md`、`source-verification.md`。本文件区分官方文档能力、课程方法和当前实例运行证据。

## 可以讲的范围

- 监控信号可以作为调查入口：错误率、延迟、成本或用户反馈；信号本身不是根因。
- 调查应定位到具体 Trace/请求，并记录时间、版本、session 或 request ID 等关联条件。
- 失败分类可以按模型、工具、数据、权限、配置和环境拆分；分类是排查方法，不是自动诊断结果。
- 修复应记录代码 commit、运行版本和验证条件，再用固定 Dataset/回归样本重跑。
- 修复前后的失败样本、回归 run、告警记录和回滚门槛共同构成闭环证据。
- Dashboard 可以帮助发现异常，但不能替代原始 Trace、失败样本或修复后的回归回读。

## 当前不能证明的范围

- 官方 Dashboards/Evaluation 文档不能证明当前项目已有真实异常 Trace、根因或修复效果。
- 当前没有受保护项目 key，因此 Trace 写入、当前实例回读、回归 run、告警闭环和修复前后对照均为 `BLOCKED`。
- 一张 Dashboard 截图、历史 Trace、health/readiness 或单次成功运行不能证明修复有效、错误率下降、延迟改善或没有回归。
- 没有多样本回归和同条件对照，不能声称问题已解决、模型更稳定或生产风险已消失。

## 最小证据包

1. 异常信号的时间窗、版本和脱敏指标；
2. 本轮异常 Trace ID 与原始回读；
3. 根因分类及其依据；
4. 修复 commit、运行版本和变更摘要；
5. 固定回归 Dataset、run ID、逐 item 结果和失败样本；
6. 修复前后对照、告警状态、回滚阈值和 SHA-256 清单；
7. 逐字段 claim review，确认没有 key、secret、Authorization、PII、完整 prompt 或内网地址。

## 录制与发布门

- 课程画面可以展示示意闭环：signal → Trace → root cause → commit → regression → alert/rollback。
- 示意画面必须固定标注 `prototype / L1`；不得使用虚构错误率、延迟、回归分数或“已修复”结论。
- 只有同一问题的异常 Trace、修复 commit 和修复后回归结果能够关联且被回读后，才能使用 `verified` 语言；当前保持 `needs-review / blocked`。

## 来源与复核

- 当前脚本引用：`https://langfuse.com/docs/observability/features/dashboards`、`https://langfuse.com/docs/evaluation/experiments`。
- 录制当天重新核对页面状态、字段和当前 SDK/实例版本；HTTP 200 只证明页面可访问，不证明当前项目行为。
- 依据：`langfuse/evidence-pack-lf11-15.md` 的 LF-12 必须证据与阻塞条件；`langfuse/source-verification.md` 的官方页面与实例证据分层规则。

## 审计结论

`prototype / L1`。LF-12 可以作为方法课程制作；真实异常 Trace、修复和回归闭环在受保护运行条件满足前保持 `BLOCKED`。
