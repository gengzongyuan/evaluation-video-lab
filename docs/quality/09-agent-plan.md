# Agent 计划与交接

| 批次 | 任务 | 输出 | 状态 |
|---|---|---|---|
| 1 | V01 选题研究 | `content/agent-v01-topic.md` | done |
| 1 | V02 脚本设计 | `content/agent-v02-scripts.md` | done |
| 1 | V03 生产模板 | `content/agent-v03-format.md` | done |
| 2 | V04 事实核验单 | `content/episode-briefs.md` | running |
| 2 | V05 口播精修 | `content/voiceover-cuts.md` | running |
| 2 | V06 生产看板 | `content/production-board.md` | running |

并行依据：每个任务写入独立文件，无共享权威状态写入；主 agent 汇合后更新状态、决策、风险与验收记录。

## Langfuse 微课批次

| 任务 | 角色 | 独占输出 | 状态 |
|---|---|---|---|
| LF-01 | 课程地图 | `langfuse/curriculum-map.md` | running |
| LF-02 | 入门编剧 | `langfuse/scripts-beginner.md` | running |
| LF-03 | 评测/实验编剧 | `langfuse/scripts-evaluation.md` | running |

## Langfuse 第三轮补充

| 任务 | 产物 | 证据 |
|---|---|---|
| LF-07 | `langfuse/source-verification.md` | 5 个官方页面 HTTP 200 |
| LF-08 | `langfuse/demo-checklist-beginner.md` | 入门 1–3 集录屏与放行清单 |

## Xiaoxiao LF-01 重制验收（2026-11-22）

前置输入：`LF-01-langfuse-overview-xiaoxiao.mp4`、`LF-01-xiaoxiao.srt/.vtt`，由 LF01-R1 生成。保持 `prototype / L1`，禁止将示意包装成真实 Trace 运行。

| 任务 | 角色 | 独占输出 | 依赖 | 状态 |
|---|---|---|---|---|
| LF01-A1 | 媒体与音频独立复核 | `langfuse/lf01-xiaoxiao-media-review.md` | LF01-R1 | queued |
| LF01-A2 | 画面节奏独立复核 | `langfuse/lf01-xiaoxiao-visual-review.md` | LF01-R1 | queued |
| LF01-B1 | 字幕烧录 | `langfuse/videos/LF-01-langfuse-overview-xiaoxiao-captioned.mp4` | 主 agent 确认可用烧录工具后 | queued |

A1/A2 不修改视频、字幕、manifest、播放器或项目权威状态。主 agent 负责 B1、汇合、质量台账、提交。停止条件：任一发现不合格须明确标为 FAIL，不得只凭媒体流存在通过。

后续独立内容任务 LF14-S1：为 LF-14 SDK 与服务端版本锁定做官方来源与事实边界审计，独占写入 `langfuse/lf14-version-pinning-fact-audit.md`。不修改 manifest、播放器、视频或权威质量状态。以官方文档为准，记录可证明和不可证明的范围。

## Xiaoxiao 连续样片批次 2（2026-11-22）

| 任务 | 角色 | 独占输出 | 状态 |
|---|---|---|---|
| LF02-R2 | LF-02 原速 Xiaoxiao 成片 | `langfuse/scripts/render_lf02_xiaoxiao_v3.py`、`langfuse/videos/LF-02-trace-xiaoxiao-v3.mp4`、`langfuse/captions/LF-02-xiaoxiao-v3.srt/.vtt`、`langfuse/lf02-xiaoxiao-v3-qa.md` | running |
| LF16-S1 | v4 OTEL 迁移事实边界 | `langfuse/lf16-v4-otel-migration-fact-audit.md` | running |
| GATE-S2 | 原速与字幕一致性门禁 | `langfuse/scripts/check_natural_voice_video.py`、`langfuse/natural-voice-quality-gate.md` | running |

后续批次（在前置独立任务完成并汇合后开始）：

| 任务 | 角色 | 独占输出 | 状态 |
|---|---|---|---|
| LF17-S1 | health/readiness 事实审计 | `langfuse/lf17-health-readiness-fact-audit.md` | queued |
| LF18-S1 | gateway readiness 事实审计 | `langfuse/lf18-gateway-readiness-fact-audit.md` | queued |

LF02-R2 的输入 `LF-02-voice-script-xiaoxiao.md` 和 `LF-02-shot-board-xiaoxiao.md` 已冻结。使用原速分段 Xiaoxiao，不拉伸补到 180 秒。只写上述独占文件，不改播放器、manifest、质量状态。主 agent 在汇合后抽帧、核对尾部静音和字幕时间轴，再决定是否登记。
