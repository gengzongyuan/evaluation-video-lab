# LF-12《从异常 Trace 到修复和回归》Xiaoxiao 分镜板

用途：按 `zh-CN-XiaoxiaoNeural`、`rate=-5%` 为 20 段口播制作画面。口播多长，成片就多长；禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

## 制作规则

- 20 镜使用 20 种不同构图，相邻构图不得重复。
- 每镜画面内只烧一条短字幕，完整口播保留在「口播」列。
- 异常指标、Trace、根因、commit、回归结果和告警均为示意或留空。
- 没有同轮写入、回读和回归证据，不使用“已修复”“已稳定”或“错误率下降”。
- 无内网地址、密钥、Authorization 值、PII、完整 Prompt 或真实业务输入输出。

## 20 镜分镜

| 镜 | 构图 | 时长提示 | 口播 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | 错误率突然上升，你能直接说根因是模型吗？不能。监控信号只是调查入口。 | 异常曲线上冲，旁边“模型根因？”被打问号 | 异常信号不是根因结论 |
| 02 | `signal-card` | 6–10s | 先记下异常发生的时间窗口、版本和指标口径。没有这些条件，两次图表可能根本不是一回事。 | 信号卡包含时间窗、版本、指标定义，不填虚构数值 | 先固定时间窗、版本和指标口径 |
| 03 | `trace-pick` | 6–10s | 从异常分组进入一条具体 Trace，保存本次 Trace ID 和原始回读，不要只截 Dashboard。 | Dashboard 异常点指向原始 Trace，截图退到辅助证据区 | 从异常分组进入原始 Trace |
| 04 | `waterfall` | 6–10s | 展开调用树和时间瀑布，先定位失败发生在哪个节点、哪一步开始偏离预期。 | 树与时间瀑布并排，失败节点高亮 | 先定位失败节点和偏离起点 |
| 05 | `inspect` | 6–10s | 核对失败节点的输入、输出、错误、状态和耗时，区分真正报错与结果不符合预期。 | 字段检查卡逐项打开，错误与低质量分开 | 核对输入、输出、错误和状态 |
| 06 | `root-cause-grid` | 6–10s | 再按模型、工具、数据、权限、配置和环境分类排查。分类是方法，不是自动诊断。 | 六类根因候选网格，均未提前下结论 | 根因分类，不等于自动找到根因 |
| 07 | `hypothesis-evidence` | 6–10s | 每个根因假设都要有证据支持，也要能被反驳。不要因为某个节点最慢，就直接认定它是根因。 | 假设与证据两栏，慢节点旁保留反例入口 | 假设需要证据，也需要可反驳 |
| 08 | `commit-card` | 6–10s | 修复时记录代码 commit、变更摘要和运行版本，让修复点能够被回指。 | commit 卡只显示脱敏占位，连接变更摘要与版本 | 修复必须对应具体 commit 和版本 |
| 09 | `isolation-gate` | 6–10s | 先控制修复范围，不要同时换 Prompt、模型和数据。否则即使结果变化，也很难归因。 | 变更闸门只允许一个变量通过，其他变更被锁住 | 修复时只改一个变量，避免混杂 |
| 10 | `dataset-return` | 6–10s | 把原始失败样本经脱敏和审核加入固定回归集，保留来源和稳定 item ID。 | 失败样本进入回归 Dataset，来源与 item ID 跟随 | 失败样本进入固定回归集 |
| 11 | `freeze-regression` | 6–10s | 回归前固定 Dataset、模型、Prompt、参数和评分规则，避免修一个问题又换了一套题。 | 五项回归配置锁定，原始失败样本不可被替换 | 回归要固定同一组题和评分规则 |
| 12 | `rerun-candidate` | 6–10s | 用修复版本重新跑同一回归集，保存新的 run 标识、逐 item 输出和运行时间。 | 修复版本进入新 run，原始输出逐条保存 | 修复后用同一回归集重跑 |
| 13 | `before-after` | 6–10s | 修复前后逐条对照，确认原失败样本真的变化，而不是只让平均分看起来更好。 | 原失败样本 before / after 并排，结果待真实运行 | 原失败样本要逐条前后对照 |
| 14 | `new-failure` | 6–10s | 同时检查新增失败和关键场景回退。修好一条样本，不代表没有碰坏别的地方。 | 已修复样本旁出现新增失败检查区 | 还要看新增失败和关键场景回退 |
| 15 | `readback-loop` | 6–10s | 用同一 run 和 item 关联回读修复后的 Score、输出和错误，让修复证据闭合。 | 修复 run → item → Score/输出/错误回读闭环 | 同一 run、item 回读修复结果 |
| 16 | `rollback-threshold` | 6–10s | 告警和回滚门槛要在发布前定义。出现关键回退时，知道谁决策、退回哪个版本。 | 回滚阈值卡连接负责人和上一版本，不填示意数字 | 发布前定义告警、回滚和责任人 |
| 17 | `trend-boundary` | 6–10s | 一次成功重跑只能说明这一次。长期稳定仍要持续观察，不能从单条结果推出来。 | 单个成功点旁长期趋势留白，标「仍需观察」 | 一次回归成功 ≠ 长期稳定 |
| 18 | `release-gate` | 6–10s | 只有异常 Trace、修复 commit 和修复后回归能关联并回读，才有理由进入发布复核。 | 三类证据共同进入发布门，缺一项门保持关闭 | 三类证据齐全，才进入发布复核 |
| 19 | `stamp` | 6–10s | 本集画面是 prototype、L1 示意，不代表当前实例已完成异常定位、修复或回归验证。 | PROTOTYPE / L1 印章，定位、修复、回归均标未证明 | prototype / L1：不是修复已验证 |
| 20 | `cta` | 6–10s | 下一集讲自托管架构：Web、Worker、数据库、Redis 和对象存储，健康检查分别能证明什么？ | LF-13 预告卡：五个组件围绕 health/readiness，不标通过 | 下一集：自托管架构与健康检查 |

## 固定构图顺序

`hook → signal-card → trace-pick → waterfall → inspect → root-cause-grid → hypothesis-evidence → commit-card → isolation-gate → dataset-return → freeze-regression → rerun-candidate → before-after → new-failure → readback-loop → rollback-threshold → trend-boundary → release-gate → stamp → cta`

## 字幕与旁白

- 声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`，禁止整段变速。
- 首次出现保留英文并给中文解释：Trace 运行记录、run 实验运行、Score 评分、commit 代码版本。
- 烧录字幕使用表中短句；SRT、VTT 使用同一时间轴，最后一条与片尾对齐。
- 不编造错误率、根因、commit、回归分数、告警状态或修复效果。

## 演示与证据边界

1. 保存异常时间窗、版本、指标口径、本轮 Trace ID 和原始回读。
2. 根因分类是排查方法；修复需对应 commit、运行版本和受控变更。
3. 固定回归 Dataset 与评分规则，保存修复前后逐 item 结果和新增失败。
4. 同轮回归回读、告警和回滚证据缺失时保持 `BLOCKED`。
5. 当前文件只定义概念课画面，不证明当前实例已定位、修复或稳定。

## 官方来源（录制当天复核）

- Dashboards：https://langfuse.com/docs/observability/features/dashboards
- Experiments：https://langfuse.com/docs/evaluation/experiments
