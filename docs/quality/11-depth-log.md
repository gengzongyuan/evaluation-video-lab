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
| 0 | 2026-11-22 | LF-19/LF-20 视频化和 LF-21 Dataset/Score 课程能否继续下钻？ | LF-01–LF-20 课程/视频/字幕、LF-21 脚本、4.79.0 runtime 探针、raw SHA-256 清单 | LF-19/LF-20 新增 180 秒 MP4 与 SRT/VTT；LF-21 新增 180 秒课程脚本；manifest/player 扩展到 21 集；来源与发布门审计完成 | 20 集原型资产可播放且均有音视频流；LF-21 脚本可录制；OTEL 入口存在；health/readiness 采样可追溯；无敏感凭据进入仓库 | 无项目 key 时不能证明 OTEL 认证成功、Trace/Score/Dataset 写入、Worker 消费、UI/API 回读或实时延迟 | 阶段保持 in_progress；成熟度保持 precheckable；Goal 保持 active | 真实运行依赖受保护凭据和锁定版本，LF-21 下一步是视频化 | 如何在脱敏和最小权限条件下获取同一 run 的 Dataset/Score 回读证据，并把 LF-21 变成可播放原型？ | 待用户/环境提供受保护运行条件 |

## 持续规则

- 阶段 `done` 不等于 Goal `complete`。
- 阻塞只阻止依赖该问题的动作，不自动结束 Goal。
- 没有真实证据时，保持当前成熟度，不把 `not_proven` 写成成熟度。
- 只有用户明确要求结束，才允许记录 Goal complete。
