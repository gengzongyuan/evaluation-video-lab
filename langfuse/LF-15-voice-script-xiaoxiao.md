# LF-15《视频与实验发布门禁》口播稿（Xiaoxiao Neural）

## 一句话结果

看完能区分“课程视频可以发布”和“Langfuse 实验变更可以发布”，并在平均分变高时仍检查关键 case 回退、同一对象回读和失败处置。

## 口播分镜（20 段，约 6–10 秒一段）

| 段 | 口播 |
|---:|---|
| 01 | 新版本平均分变高，就一定能上线吗？不一定。关键 case，可能刚刚从对变错。 |
| 02 | 先分清两道门：视频能不能发，实验变更能不能上线。它们查的不是同一件事。 |
| 03 | 先说实验门。固定同一版 Dataset，数据集；用同一套评估器，再比较批准的基线和候选版本。 |
| 04 | Dataset 版本固定的是测试题。模型输出并不因此固定，更不能拿两套试卷比总分。 |
| 05 | 基线也别默认选最新一次 run。最新运行可能已经失败；真正的基线，要先审查，再明确批准。 |
| 06 | 然后看关键 case。普通题修好了，退款期限却答错了，平均分再高，也要停下来查。 |
| 07 | 这就是平均分的陷阱：它可能把改对两题、弄错一题，算成总体进步。 |
| 08 | 发布前先问四句：数据同版吗？评估器同版吗？关键 case 回退了吗？失败有人审过吗？ |
| 09 | 再收紧一点：必需 case 必须通过；基线通过的 case，候选不能无缘无故弄坏。 |
| 10 | 缺 case、重复 ID、任务报错、评估器没结果，都不能算通过。缺证据，就先拦住。 |
| 11 | Score，分数，也不是装饰。要看到它挂在哪个 run、哪个 item，谁评的，用哪版规则评的。 |
| 12 | 打开变差的 case，回到 Trace，追踪记录，看检索、工具和模型。先找根因，再决定修代码还是修评估器。 |
| 13 | 改动评估器后，基线和候选都要按新定义重算。只重算一边，比较就失去共同尺度。 |
| 14 | 发布 Prompt，提示词时，production 标签只是指向某个版本。它不是质量、成本或安全的合格证。 |
| 15 | 换到视频门：画面清楚、字幕齐全，只证明成片能看，不证明里面的 Langfuse 实验跑过。 |
| 16 | 页面截图、health 200、甚至视频播放正常，都不能替代同一个 run 的写入和回读。 |
| 17 | 所以发布视频前，要让脚本、成片、字幕、素材和 manifest 清单指向同一 commit，能回滚，也做过脱敏。 |
| 18 | 目前没有可核验的项目 key，没有真实 run 和 Score 回读。本片只讲发布方法，保留 prototype、L1 示意。 |
| 19 | 真正放行时，把 Dataset 版本、基线 run、候选 run、评估器版本和失败处置，放进同一份证据包。 |
| 20 | 下一集讲 v4 和 OTEL 迁移：换了写入方式，怎么证明新 Trace 真到了，也能按 ID 读回来？ |

## 配音约定

- 固定 `zh-CN-XiaoxiaoNeural`、`rate=-5%`。按每段实际音频时长切镜头，禁止把整段音频拉伸到 180 秒，也禁止用尾部静音凑时长。
- 读法：Dataset 读“Dataset，数据集”；case 读英文“case”，保留“关键 case”的说法；run 读英文“run”；Score 读“Score，分数”；Trace 读“Trace，追踪记录”；Prompt 读“Prompt，提示词”；OTEL 读“O-TEL”；`prototype / L1` 口播读“prototype，L1 示意”。
- “case”“run”“item”第一次出现时在画面字幕附中英对照，后续可只显示英文。不要逐字母拼读。
- 第 01 段稍慢，突出“平均分变高”和“不一定”的反差；第 06–10 段按短句落点停顿，不把四句检查念成一口气。
- 字幕跟随实际语音切分，每屏一到两行；独立 SRT/VTT 使用同一时间轴，成片同时烧录字幕。

## 画面提示（20 镜，供重剪）

| 段 | 构图与信息变化 |
|---:|---|
| 01 | 上行平均分曲线旁，一条关键 case 从 Pass 翻成 Fail。 |
| 02 | 两扇并列门：视频发布门 / 实验发布门，分别列出检查对象。 |
| 03 | 同一 Dataset 版本、同一评估器汇入“基线 vs 候选”比较槽。 |
| 04 | 同一份试卷盖上版本章；旁边提示“输出仍可能变化”。 |
| 05 | 时间线上“最新 run”被移开，另把已审查 run 钉为基线。 |
| 06 | 两题变绿、关键退款题变红；平均分箭头不能遮住红色格。 |
| 07 | 放大一个变红格子，解释平均数如何掩盖它。 |
| 08 | 四问按口播依次出现，最后收进一张发布前检查卡。 |
| 09 | 两条规则并排：必需 case 必过 / 已批准通过不得回退。 |
| 10 | 缺 case、重复 ID、任务报错、无评分依次触发红色阻断。 |
| 11 | Score 卡连向 run、item、评分来源、评估器版本四个锚点。 |
| 12 | 从红色 case 钻入 Trace 树，定位检索、工具或模型节点。 |
| 13 | 两侧同时换用新评估器并重新评分，禁止只刷新候选一侧。 |
| 14 | production 标签指向 Prompt 版本，旁边“不等于验收”保持可见。 |
| 15 | 清晰画面与字幕通过媒体门；实验门仍显示 BLOCKED。 |
| 16 | 截图、health 200、播放正常三张卡，都不能替代 run 写入与回读。 |
| 17 | 脚本、成片、字幕、素材、manifest 汇入同一 commit；标出脱敏与回滚。 |
| 18 | prototype / L1 状态卡；明确没有真实 run 或 Score 回读。 |
| 19 | 证据包目录：Dataset 版本、两条 run ID、评估器版本、失败处置。 |
| 20 | 下一集预告：v4 / OTEL 迁移 → 新 Trace → 同 ID 回读。 |

## 事实边界

- 全片保持 `prototype / L1`。本稿只讲方法、反例和放行条件，不伪造 Dataset run、Score、Prompt 部署或 CI 通过。
- 实验门与视频门不能互相替代。媒体门 PASS、页面能打开、health 200 或截图存在，都不证明当前实例已写入和回读实验结果。
- “必需 case 通过”和“已批准通过的 case 不得回退”是发布政策，不是 Langfuse 自动保证业务正确；已知失败需要明确审查与接受。
- 固定 Dataset 版本只固定测试数据，不保证模型输出确定。改动评估器后，基线和候选要使用相同的新定义重算。
- 真实放行还需记录模型与应用版本、run 时间、Score 错误、脱敏结果和回滚点；本稿不宣称当前仓库已有 CI 门禁。
- 公开视频不得出现内网地址、项目密钥、Authorization 值、登录信息、PII 或完整未脱敏的 Prompt / 输出。

## 官方来源（2026-11-23 复核）

- Compare experiments：https://langfuse.com/docs/evaluation/experiments/compare-experiments
- Experiments in CI/CD：https://langfuse.com/docs/evaluation/experiments/experiments-ci-cd
- Datasets：https://langfuse.com/docs/evaluation/experiments/datasets
- Scores：https://langfuse.com/docs/observability/features/scores
- Prompt version control：https://langfuse.com/docs/prompt-management/features/prompt-version-control

对照审计：`langfuse/lf15-release-gate-fact-audit.md`。官方页面可访问只证明文档口径可回指，不证明当前实例运行成功。
