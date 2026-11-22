# LF-15《视频与实验发布门禁》Xiaoxiao 分镜板

用途：按 `zh-CN-XiaoxiaoNeural`、`rate=-5%` 为 20 段口播制作画面。口播多长，成片就多长；禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

## 制作规则

- 20 镜使用 20 种不同构图，相邻构图不得重复。
- 每镜画面内只烧一条短字幕，完整口播保留在「口播」列。
- 分数、case、run ID、Prompt 版本和放行状态均为示意或留空。
- 视频发布门与实验发布门不能互相替代，媒体 PASS 不证明 Langfuse 实验成功。
- 无内网地址、密钥、Authorization 值、登录信息、PII 或完整未脱敏 Prompt。

## 20 镜分镜

| 镜 | 构图 | 时长提示 | 口播 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | 新版本平均分变高，就一定能上线吗？不一定。关键 case，可能刚刚从对变错。 | 上行平均分曲线旁，关键 case 从 Pass 翻成 Fail | 平均分变高，也不一定能上线 |
| 02 | `dual-gates` | 6–10s | 先分清两道门：视频能不能发，实验变更能不能上线。它们查的不是同一件事。 | 视频发布门 / 实验发布门并列，分别列检查对象 | 视频能发和实验能上线是两道门 |
| 03 | `frozen-input` | 6–10s | 先说实验门。固定同一版 Dataset，用同一套评估器，再比较批准的基线和候选版本。 | 同版 Dataset 与同评估器汇入基线/候选比较槽 | 同版 Dataset、同评估器再比较 |
| 04 | `versioned-paper` | 6–10s | Dataset 版本固定的是测试题。模型输出并不因此固定，更不能拿两套试卷比总分。 | 同一份试卷盖版本章，输出端仍有波动符号 | 固定测试题，不等于固定模型输出 |
| 05 | `baseline-approval` | 6–10s | 基线别默认选最新一次 run。最新运行可能已经失败；真正的基线，要先审查，再明确批准。 | 时间线上最新 run 被移开，已审查 run 钉为基线 | 最新 run 不等于已批准基线 |
| 06 | `critical-case` | 6–10s | 然后看关键 case。普通题修好了，关键场景却答错了，平均分再高，也要停下来查。 | 普通题变绿，关键 case 变红，红色不可被总分遮住 | 关键 case 回退，平均分高也要停 |
| 07 | `average-mask` | 6–10s | 这就是平均分的陷阱：它可能把改对两题、弄错一题，算成总体进步。 | 放大变红格子，平均数遮罩被揭开 | 平均数可能掩盖单点回退 |
| 08 | `four-questions` | 6–10s | 发布前先问四句：数据同版吗？评估器同版吗？关键 case 回退了吗？失败有人审过吗？ | 四问依次出现，最后收进发布检查卡 | 数据、评估器、回退、失败审查四问 |
| 09 | `policy-pair` | 6–10s | 再收紧一点：必需 case 必须通过；基线通过的 case，候选不能无缘无故弄坏。 | 两条政策并排：required-pass / no-regression | 必需项必过，已通过项不能回退 |
| 10 | `blocker-stack` | 6–10s | 缺 case、重复 ID、任务报错、评估器没结果，都不能算通过。缺证据，就先拦住。 | 四类阻断依次落锁，没有一项被算成通过 | 缺 case、报错、无评分都不能通过 |
| 11 | `score-anchor` | 6–10s | Score 不是装饰。要看到它挂在哪个 run、哪个 item，谁评的，用哪版规则评的。 | Score 卡连接 run、item、来源、评估器版本四个锚点 | Score 要追到对象、来源和规则版本 |
| 12 | `trace-drill` | 6–10s | 打开变差的 case，回到 Trace，看检索、工具和模型。先找根因，再决定修代码还是修评估器。 | 红色 case 钻入 Trace 树，失败节点高亮 | 从变差 case 回到原始 Trace |
| 13 | `recalc-both` | 6–10s | 改动评估器后，基线和候选都要按新定义重算。只重算一边，比较就失去共同尺度。 | 基线与候选同时刷新新评估器，单边刷新被打叉 | 评估器变了，两边都要重算 |
| 14 | `label-pointer` | 6–10s | 发布 Prompt 时，production 标签只是指向某个版本。它不是质量、成本或安全的合格证。 | production 指针指向版本卡，三项验收仍待检查 | production 标签不是验收合格证 |
| 15 | `media-pass` | 6–10s | 换到视频门：画面清楚、字幕齐全，只证明成片能看，不证明里面的 Langfuse 实验跑过。 | 媒体门 PASS，实验门仍显示 BLOCKED | 媒体 PASS ≠ 实验已跑通 |
| 16 | `evidence-boundary` | 6–10s | 页面截图、health 200、甚至视频播放正常，都不能替代同一个 run 的写入和回读。 | 截图、health、播放三张卡停在写入/回读边界外 | 截图和 health 不能替代 run 回读 |
| 17 | `commit-bundle` | 6–10s | 发布视频前，让脚本、成片、字幕、素材和 manifest 指向同一 commit，能回滚，也做过脱敏。 | 五类资产汇入同一 commit，脱敏与回滚为必经节点 | 脚本、成片、字幕和清单同版可回滚 |
| 18 | `stamp` | 6–10s | 目前没有可核验的项目权限，没有真实 run 和 Score 回读。本片只讲发布方法，保留 prototype、L1 示意。 | PROTOTYPE / L1 印章，run 与 Score 回读均标未证明 | prototype / L1：没有真实 run 和 Score 回读 |
| 19 | `evidence-pack` | 6–10s | 真正放行时，把 Dataset 版本、基线 run、候选 run、评估器版本和失败处置放进同一份证据包。 | 证据包目录五项齐全，缺失时发布门保持关闭 | 版本、两条 run、评估器、失败处置同包 |
| 20 | `cta` | 6–10s | 下一集讲 v4 和 OTEL 迁移：换了写入方式，怎么证明新 Trace 真到了，也能按 ID 读回来？ | LF-16 预告：v4/OTEL → 新 Trace → 同 ID 回读 | 下一集：v4 和 OTEL 迁移怎么验收 |

## 固定构图顺序

`hook → dual-gates → frozen-input → versioned-paper → baseline-approval → critical-case → average-mask → four-questions → policy-pair → blocker-stack → score-anchor → trace-drill → recalc-both → label-pointer → media-pass → evidence-boundary → commit-bundle → stamp → evidence-pack → cta`

## 字幕与旁白

- 声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`，禁止整段变速。
- 首次出现中英并读：Dataset 数据集、run 实验运行、Score 评分、Trace 运行记录、Prompt 提示词。
- 烧录字幕使用表中短句；SRT、VTT 使用同一时间轴，最后一条与片尾对齐。
- 不伪造 Dataset run、Score、Prompt 部署、CI 通过或真实分数。

## 演示与证据边界

1. 实验门固定 Dataset/evaluator 版本、已批准基线、候选、模型/应用版本和发布政策。
2. 缺失 case、重复 ID、任务失败、无评分都不能算通过；改动评估器后两边都重算。
3. 视频门要求脚本、成片、字幕、素材、manifest 同一 commit，脱敏并可回滚。
4. 真实放行需同一 run/item 的 Score、输出、错误和回读；媒体与 health 均不能替代。
5. 当前文件只定义概念课画面，不证明当前实例或当前仓库已通过任一门禁。

## 官方来源（录制当天复核）

- Compare experiments：https://langfuse.com/docs/evaluation/experiments/compare-experiments
- Experiments in CI/CD：https://langfuse.com/docs/evaluation/experiments/experiments-ci-cd
- Datasets：https://langfuse.com/docs/evaluation/experiments/datasets
- Scores：https://langfuse.com/docs/observability/features/scores
- Prompt version control：https://langfuse.com/docs/prompt-management/features/prompt-version-control
