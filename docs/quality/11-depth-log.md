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
| 1 | 2026-11-22 | 快切样片能否达到真实短视频的基本音画门？ | LF-01/LF-02/LF-03 v2、自动质量门、字幕审计 | LF-01–LF-03 快切样片；质量门脚本；LF-02 字幕时间码/乱码修复；播放器接入 LF-03 v2 | 三集均约 180 秒、12 个镜头、非静音中文 TTS、抽帧有变化、字幕文件存在；媒体门通过 | 仍未证明人工听感、字幕逐字同步、真实 UI 录屏或 Langfuse 当前实例写入/回读 | 课程生产门从“可播放”提升为“快切媒体门”；Goal 保持 active | 下一步批量推进 LF-04 Prompt 管理，同时保留人工内容审�� | LF-04 的 Prompt 版本/label 如何用同样节奏讲清并避免把示意画面说成真实 UI？ | 待下一轮内容与来源审计 |
| 2 | 2026-11-22 | Dataset 与 Score 能否用同一快切门讲清可复核证据？ | LF-04/LF-05/LF-06 v2、事实审计、字幕审计、媒体质量门 | LF-04–LF-06 快切样片；LF-05 Dataset 事实审计；LF-06 Score 事实审计；播放器接入 LF-06 | 六集快切媒体门通过；LF-05/06 明确 item/run/score/失败样本和 BLOCKED 边界；manifest 保持通过 | 真实 Dataset run、Score 写入/回读、人工听感和真实 UI 仍未验证 | 课程线完成 Prompt→Dataset→Score 的第一条可连续观看样片链 | 下一步推进 LF-07 成本、token usage 和延迟，并继续隔离媒体门与运行证据门 | 如何讲清成本/延迟字段而不把示意数字说成当前实例测量？ | 待下一轮来源与样片审计 |
| 4 | 2026-11-22 | 选定的 Xiaoxiao 能否做成可直接看的原速短视频？ | 失败的拉伸版 Xiaoxiao、20 段口播稿、独立音画 FAIL | v3：168.7 秒、24 镜、画面内字幕、原速 AAC；播放器改链；LF-02 口播稿、LF-14/15 事实审计 | 原速旁白、烧录字幕、镜头构图变化、音视频对齐 | 真实 Langfuse 写入/回读、人工听感终审、其余 20 集尚未用同一声线重做 | 课程生产从“有 AAC 的卡片片”转为“原速神经 TTS + 画面内字幕”；Goal 保持 active | ffmpeg scene=0.08 对深色卡片不敏感，不能单独当切镜门 | 下一集 Trace vs 日志能否用同一 Xiaoxiao 原速流程重做？ | 用户已选定 Xiaoxiao |
| 3 | 2026-11-22 | 生产治理能否用快切讲清“配置能力不等于已安全”？ | LF-07/LF-08/LF-09 v2、事实审计、敏感信息检查、媒体质量门 | LF-07–LF-09 快切样片；LF-09 sampling/脱敏/保留/权限/告警审计；播放器接入 LF-09；修复 LF-09 字幕乱码 | 九集快切媒体门通过；LF-09 未暴露内网地址、key、secret、Authorization 或 PII；治理结论保持 prototype/L1 | 当前部署的 redaction、retention、权限审计、告警闭环和真实运行仍未验证 | 课程线完成 Score→成本→反馈→生产治理的连续样片链；Goal 保持 active | 下一步推进 LF-10 多步骤 Agent 调用树，并核对真实调用树证据边界 | 如何展示 Agent 调用树的决策、Tool 和 Generation 而不把示意树说成当前实例 Trace？ | 待下一轮来源与样片审计 |

| 5 | 2026-11-23 | 选定 Xiaoxiao 后，原速分段配音加画面内字幕能否连续做出可看的入门课？ | 失败拉伸版 Xiaoxiao、LF-01 v3 乱码第 4 镜、LF-02/03 分镜、自然旁白门 | 重渲 LF-01 第 4 镜；交付 LF-02/03/07 Xiaoxiao 原速成片；播放器改链；独立抽帧与自然旁白门 PASS | LF-01 173.033s/24 镜、LF-02 161.003s/20 镜、LF-03 170.600s/20 镜、LF-07 176.233s/20 镜；画面内字幕；未拉伸；无 U+FFFD | 真实 Langfuse 写入/回读、人工听感终审、其余集尚未用同一声线重做 | 课程生产从卡片片转为 Xiaoxiao 原速 + 烧录字幕；Goal 保持 active | 媒体门 PASS 仍不能代替 Dataset/Score/OTEL 回读 | 下一集 Prompt 版本/label 如何用同一 Xiaoxiao 流程讲清，且不把 label 说成已发布或效果更好？ | 用户已选定 Xiaoxiao |
| 6 | 2026-11-23 | Prompt 版本和 Dataset 能否用同一 Xiaoxiao 原速流程讲清，且不把示意写成已发布或实验已跑通？ | LF-04/LF-05 分镜、独立复核、自然旁白门 | 交付 LF-04/LF-05 Xiaoxiao 原速成片；播放器改链；LF-04 独立复核 PASS；LF-05 主 agent 抽帧 PASS | LF-04 166.866s/20 镜、LF-05 173.071s/20 镜；画面内字幕；未拉伸；无 U+FFFD | 真实 Prompt/Dataset/Score 写入与回读、人工听感终审、LF-06 尚未重做 | Xiaoxiao 原速样片覆盖入门到 Dataset；Goal 保持 active | 媒体门 PASS 仍不能代替 Dataset run | 下一集 Score 与失败样本如何用同一流程讲清，且不把示意分数说成当前实例评分？ | 用户已选定 Xiaoxiao |

## 持续规则

- 阶段 `done` 不等于 Goal `complete`。
- 阻塞只阻止依赖该问题的动作，不自动结束 Goal。
- 没有真实证据时，保持当前成熟度，不把 `not_proven` 写成成熟度。
- 只有用户明确要求结束，才允许记录 Goal complete。
