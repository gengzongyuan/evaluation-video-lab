# 长期 Goal 下钻台账

本文件只在 `continuity_mode: sustained-goal` 下使用。它记录每轮真实推进和下一层问题，不替代 `00-project-state.md`、阶段文档或 Goal 本身。

## Goal 摘要

- Goal 引用：
- Goal 目标：
- 生命周期：pending_goal_initialization/active/paused/用户明确结束
- 当前下钻轮次：0
- 当前阶段：
- 当前成熟度：not_assessed

## 下钻记录

| 轮次 | 日期 | 本轮问题 | 输入快照 | 本轮事实/产物 | 已证明范围 | 未证明范围 | 状态变化 | 开放冲突 | 下一层问题 | 用户决策 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 2026-11-22 | LF-19/LF-20 课程和 LAB-02 证据能否继续下钻？ | LF-01–LF-18 资产、4.79.0 runtime 探针、raw SHA-256 清单 | 新增 LF-19/LF-20 课程设计；完成 raw 完整性审计和系列缺口审计 | 18 集原型资产完整；OTEL 入口存在；health/readiness 采样可追溯；无敏感凭据进入仓库 | 无项目 key 时不能证明 OTEL 认证成功、Trace 写入、Worker 消费、UI/API 回读或实时延迟 | 阶段保持 in_progress；成熟度保持 precheckable；Goal 保持 active | 课程脚本可继续扩展，但真实演示依赖受保护凭据和锁定版本 | 如何在脱敏和最小权限条件下获取 Trace ID 回读及时间戳证据？ | 待用户/环境提供受保���运行条件 |

## 持续规则

- 阶段 `done` 不等于 Goal `complete`。
- 阻塞只阻止依赖该问题的动作，不自动结束 Goal。
- 没有真实证据时，保持当前成熟度，不把 `not_proven` 写成成熟度。
- 只有用户明确要求结束，才允许记录 Goal complete。
