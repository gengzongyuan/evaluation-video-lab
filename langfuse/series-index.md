# Langfuse 3 分钟微课系列索引

核对日期：2026-11-22（Asia/Shanghai）。状态以仓库文件为准：`prototype` 表示有可播放原型；`scripted` 表示有脚本/知识卡但尚未生成视频；`blocked` 表示真实实例证据未满足。

| 集数 | 标题 | 层级 | 脚本/知识卡 | 视频 | 状态 | 证据等级 |
|---|---|---|---|---|---|---|
| LF-01 | Langfuse 是什么 | 入门 | `episodes/LF-01-script.md`、`scripts-beginner.md` | `videos/LF-01-langfuse-overview-prototype.mp4` | prototype | L1 |
| LF-02 | Trace 是什么 | 入门 | `scripts-beginner.md`、`lf02-evidence-record.md` | `videos/LF-02-trace-prototype.mp4` | prototype | L1 |
| LF-03 | Span / Generation / Tool / Agent | 入门 | `lf03-type-card.md`、`lf03-script-revision.md` | `videos/LF-03-span-generation-prototype.mp4` | prototype | L1 |
| LF-04 | Prompt 管理、版本和 label | 基础 | `lf04-prompt-lesson.md` | `videos/LF-04-prompt-management-prototype.mp4` | prototype | L1 |
| LF-05 | Dataset 与可重复实验 | 进阶 | `lf05-dataset-lesson.md` | — | scripted | L1 |
| LF-06 | Evaluation、Score 与失败样本 | 进阶 | `lf06-score-lesson.md` | — | scripted | L1 |
| LF-07 | 成本、token usage 和延迟 | 进阶 | `lf07-cost-latency-lesson.md`、`scripts-production.md` | `videos/LF-07-cost-latency-prototype.mp4` | prototype | L1 |
| LF-08 | 用户反馈回流 Score | 进阶 | `lf08-feedback-lesson.md` | — | scripted | L1 |
| LF-09 | Sampling、脱敏、保留和治理 | 生产 | `lf09-production-governance-lesson.md`、`scripts-production.md` | — | scripted | L1 |
| LF-10 | 多步骤 Agent 调用树 | 生产 | `lf10-agent-observability-lesson.md` | `videos/LF-10-agent-observability-prototype.mp4` | prototype | L1 |
| LF-11 | 同 Dataset 比较 Prompt / 模型 | 进阶 | `lf11-experiment-compare-lesson.md` | — | scripted | L1 |
| LF-12 | 异常 Trace 到修复和回归 | 生产 | `lf12-debugging-loop-lesson.md` | — | scripted | L1 |
| LF-13 | 自托管架构与健康检查 | 生产 | `lf13-self-hosting-lesson.md` | `videos/LF-13-self-hosting-prototype.mp4` | prototype | L1 |
| LF-14 | SDK 与服务端版本��定 | 生产 | `lf14-sdk-version-lesson.md` | — | scripted | L1 |
| LF-15 | 视频与实验发布门禁 | 生产 | `lf15-release-gate-lesson.md` | — | scripted | L1 |

## 发布顺序

先发布 LF-01 → LF-04，建立 Trace 和 Prompt 心智模型；再发布 LF-05 → LF-08，进入 Dataset、Score、成本和反馈；最后发布 LF-09 → LF-15，讲生产、治理和发布质量。所有 `prototype` 仍需替换真实 UI/录屏并完成事实核验，不能直接宣称为产品实测结论。
| LF-16 | Langfuse v4：旧 API 为什么失效？ | 迁移 | `lf16-v4-otel-migration-lesson.md` | `videos/LF-16-v4-otel-migration-prototype.mp4` | prototype | L1 |
| LF-17 | Health 通过，为什么链路还不能用？ | 生产 | `lf17-health-readiness-lesson.md` | `videos/LF-17-health-readiness-prototype.mp4` | prototype | L1 |
