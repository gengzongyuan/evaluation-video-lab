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

## Xiaoxiao 连续样片批次 3（2026-11-23）

当前阶段：内容生产与媒体验证，`in_progress`。冻结契约：中文声线 `zh-CN-XiaoxiaoNeural`、`rate=-5%`；原速分段配音；每集由实际语音决定时长；约 20–24 个不同构图，通常每 6–10 秒明显变化；视频内直接烧录中文字幕并保留同时间轴 SRT/VTT；课程均为 `prototype / L1`，无项目 key 时不得声称真实 Trace、Dataset、Score、Worker 消费或回读已验证。

| id | stage | role | goal | inputs | depends_on | write_scope | forbidden_write | shared_resources | verification | output | status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LF02-R3 | implementation + verification | 视频制作 | 交付可播放的 LF-02 原速 Xiaoxiao 成片、内嵌字幕及制作脚本 | 已冻结的 `langfuse/LF-02-voice-script-xiaoxiao.md`、`langfuse/LF-02-shot-board-xiaoxiao.md`；参考 `langfuse/scripts/render_lf01_xiaoxiao_v3.py` | 无 | `langfuse/scripts/render_lf02_xiaoxiao_v3.py`、`langfuse/videos/LF-02-trace-xiaoxiao-v3.mp4`、`langfuse/captions/LF-02-xiaoxiao-v3.srt`、`langfuse/captions/LF-02-xiaoxiao-v3.vtt`、`langfuse/lf02-xiaoxiao-v3-qa.md`、`langfuse/build/lf02-xiaoxiao-v3/` | 播放器、manifest、课程索引、质量状态、其他任务文件；不得 git commit/push | 本机 Edge TTS、ffmpeg@7；不得访问或写入真实 Langfuse 项目 | 运行自然旁白门；抽帧；检查 U+FFFD、字幕覆盖/结束时间、尾部静音、音视频时长差、唯一镜头数 | 上述成片、字幕、渲染器、QA 与固定格式交接 | running |
| LF03-S4 | requirements + content | 口播与事实校对 | 把 LF-03 分镜冻结为适合 Xiaoxiao 的逐镜口播，并核验类型与证据边界 | `langfuse/LF-03-shot-board-xiaoxiao.md`、`langfuse/lf03-script-revision.md`、`langfuse/lf03-type-card.md`、`langfuse/lf03-demo-plan.md` 及录制当天 Langfuse 官方文档 | 无 | `langfuse/LF-03-voice-script-xiaoxiao.md`、`langfuse/lf03-xiaoxiao-fact-audit.md` | 视频、音频、字幕、渲染器、播放器、manifest、质量状态；不得 git commit/push | 只读官方文档；无真实项目写入 | 检查逐镜编号、口播与镜头一致、无乱码/敏感值；官方 URL 与概念逐项可回指 | 两份独占文档与固定格式交接 | running |
| LF18-S1 | requirements + fact audit | 官方事实审计 | 核验 LF-18 gateway readiness 课程，区分端点可达、鉴权、Trace 写入和回读 | `langfuse/lf18-gateway-readiness-lesson.md`、`langfuse/evidence/lf18-gateway-probe.md` 及当前 Langfuse 官方文档 | 无 | `langfuse/lf18-gateway-readiness-fact-audit.md` | 视频、音频、字幕、播放器、manifest、质量状态、其他审计；不得 git commit/push | 只读官方文档和已有脱敏证据；不得触网真实项目或伪造运行结果 | 检查官方来源、事实/推断分离、无内网地址或凭据；记录能与不能证明的范围 | 独占审计文档与固定格式交接 | running |

停止条件：输入冲突、需要扩大范围或需要真实项目凭据时停止对应动作并上报，不用猜测补齐。主 agent 独占 LF-01 乱码重渲染、所有汇合、抽帧终审、索引/播放器/manifest、质量台账和 Git 提交推送。任一任务完成后，由主 agent 汇合并立即派发下一项有独立产出的任务；Goal 保持 active。

## Xiaoxiao 连续样片批次 4（2026-11-23）

| id | stage | role | goal | inputs | depends_on | write_scope | forbidden_write | shared_resources | verification | output | status |
|---|---|---|---|---|---|---|---|---|---|---|---|
| LF03-R3 | implementation + verification | 视频制作 | 交付可播放的 LF-03 原速 Xiaoxiao 成片、内嵌字幕及制作脚本 | 已冻结的 `langfuse/LF-03-shot-board-xiaoxiao.md`、`langfuse/lf03-script-revision.md`、`langfuse/lf03-type-card.md`；参考 `langfuse/scripts/render_lf01_xiaoxiao_v3.py` 与 `langfuse/scripts/render_lf02_xiaoxiao_v3.py` | 无 | `langfuse/scripts/render_lf03_xiaoxiao_v3.py`、`langfuse/videos/LF-03-span-generation-xiaoxiao-v3.mp4`、`langfuse/captions/LF-03-xiaoxiao-v3.srt`、`langfuse/captions/LF-03-xiaoxiao-v3.vtt`、`langfuse/lf03-xiaoxiao-v3-qa.md`、`langfuse/build/lf03-xiaoxiao-v3/` | 播放器、manifest、课程索引、质量状态、其他集视频/字幕；不得 git commit/push | 本机 Edge TTS、ffmpeg@7；不得访问或写入真实 Langfuse 项目 | 运行自然旁白门；抽帧；检查 U+FFFD、字幕覆盖/结束时间、尾部静音、音视频时长差、唯一镜头数 | 上述成片、字幕、渲染器、QA 与固定格式交接 | running |
| LF07-S7 | content | 分镜 | 把 LF-07 成本、token 与延迟拆成 20 段 Xiaoxiao 分镜 | `langfuse/lf07-cost-latency-lesson.md`、`langfuse/lf07-fact-audit.md`、`langfuse/lf07-v2-qa.md` | 无 | `langfuse/LF-07-shot-board-xiaoxiao.md` | 视频、音频、字幕、渲染器、播放器、manifest、质量状态；不得 git commit/push | 只读官方文档 | 20 镜连续编号、20 个唯一 layout、相邻构图不重复、无乱码/敏感值 | 独占分镜板与固定格式交接 | running |
| LF20-S1 | requirements + fact audit | 官方事实审计 | 核验 LF-20 OTEL headers 与实时性课程，区分入口可达、认证、写入、回读和实时延迟 | `langfuse/lf20-otel-headers-realtime-lesson.md`、已有脱敏探针与官方文档 | 无 | `langfuse/lf20-otel-headers-realtime-fact-audit.md` | 视频、音频、字幕、播放器、manifest、质量状态、其他审计；不得 git commit/push | 只读官方文档和已有脱敏证据；不得伪造运行结果 | 检查官方来源、事实/推断分离、无内网地址或凭据；记录能与不能证明的范围 | 独占审计文档与固定格式交接 | running |

## Xiaoxiao 连续样片批次 5（2026-11-23）

冻结契约不变：`zh-CN-XiaoxiaoNeural`、`rate=-5%`；原速分段；画面内字幕；`prototype / L1`。

| id | role | write_scope | status |
|---|---|---|---|
| LF04-R4 | 视频制作 | `langfuse/videos/LF-04-prompt-version-xiaoxiao-v3.mp4` 及字幕/渲染器/QA | done |
| LF04-A4 | 独立媒体复核 | `langfuse/lf04-xiaoxiao-v3-independent-review.md` | done |
| LF05-R5 | 视频制作 | `langfuse/videos/LF-05-dataset-xiaoxiao-v3.mp4` 及字幕/渲染器/QA | done |
| LF06-R6 | 视频制作 | `langfuse/videos/LF-06-score-xiaoxiao-v3.mp4` 及字幕/渲染器/QA | running |
| LF05-V5 | 口播冻结 | `langfuse/LF-05-voice-script-xiaoxiao.md` 到 LF-09 | running |
| SCAN-S5 | 越界话术扫描 | `langfuse/xiaoxiao-v3-claim-scan-lf05-lf21.md` | running |

主 agent 独占汇合、播放器/索引/质量台账和 Git 提交。Goal 保持 active。

## Xiaoxiao 连续样片批次 6（2026-11-23）

| id | role | write_scope | status |
|---|---|---|---|
| LF06-R6 | 视频制作 | `langfuse/videos/LF-06-score-xiaoxiao-v3.mp4` 及字幕/渲染器/QA | done |
| LF09-R9 | 视频制作 | `langfuse/videos/LF-09-governance-xiaoxiao-v3.mp4` 及字幕/渲染器/QA | done |
| LF08-R8 | 视频制作 | `langfuse/videos/LF-08-feedback-xiaoxiao-v3.mp4` 及字幕/渲染器/QA | done |
| LF10-R10 | 视频制作 | `langfuse/videos/LF-10-agent-tree-xiaoxiao-v3.mp4` 及字幕/渲染器/QA | done |
| LF11-R11 | 视频制作 | `langfuse/videos/LF-11-compare-xiaoxiao-v3.mp4` 及字幕/渲染器/QA | done |
| LF05-V5 | 口播冻结 | `langfuse/LF-11-voice-script-xiaoxiao.md` 到 LF-13 | running |
| LF08-A8 | 独立媒体复核 | `langfuse/lf08-xiaoxiao-v3-independent-review.md`、`langfuse/lf10-xiaoxiao-v3-independent-review.md` | running |

## Xiaoxiao 连续样片批次 7（2026-11-23）

冻结契约不变：`zh-CN-XiaoxiaoNeural`、`rate=-5%`；原速分段；画面内字幕；`prototype / L1`。

| id | role | write_scope | status |
|---|---|---|---|
| LF11-R11 | 视频制作 | `langfuse/videos/LF-11-compare-xiaoxiao-v3.mp4` 及字幕/渲染器/QA | done |
| LF11-V11 | 口播冻结 | `langfuse/LF-11-voice-script-xiaoxiao.md`、`langfuse/LF-12-voice-script-xiaoxiao.md`、`langfuse/LF-13-voice-script-xiaoxiao.md` | running |
| LF08-A8 | 独立媒体复核 | `langfuse/lf08-xiaoxiao-v3-independent-review.md`、`langfuse/lf10-xiaoxiao-v3-independent-review.md` | running |

## Xiaoxiao 连续样片批次 8（2026-11-23）

冻结契约不变：`zh-CN-XiaoxiaoNeural`、`rate=-5%`；原速分段；画面内字幕；`prototype / L1`。

| id | role | write_scope | status |
|---|---|---|---|
| LF12-R12 | 视频制作 | `langfuse/videos/LF-12-debug-regression-xiaoxiao-v3.mp4` 及字幕/渲染器/QA | running |
| LF11-V11 | 口播冻结 | `langfuse/LF-11-voice-script-xiaoxiao.md` 到 LF-15 | running |
| LF11-A11 | 独立媒体复核 | `langfuse/lf11-xiaoxiao-v3-independent-review.md` | running |
