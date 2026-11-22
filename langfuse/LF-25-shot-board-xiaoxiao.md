# LF-25《把 Experiment 变成 CI 发布门》Xiaoxiao 分镜板

用途：按 `zh-CN-XiaoxiaoNeural`、`rate=-5%` 为 20 段口播制作画面。口播多长，成片就多长；禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

## 制作规则

- 20 镜使用 20 种不同构图，相邻构图不得重复。
- 每镜画面内只烧一条短字幕，完整口播保留在「口播」列。
- CI 状态、case、run、分数、版本和发布结果均为示意或留空。
- 无内网地址、真实 key/secret、Authorization 值、PII 或未脱敏 Prompt。

## 20 镜分镜

| 镜 | 构图 | 时长提示 | 口播 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | CI 显示绿色，就真的可以上线吗？先看门禁有没有把缺失、报错和关键回退，错当成了通过。 | 绿色 CI 勾号被揭开，后方露出缺失、报错、回退三个洞 | CI 变绿，不一定是真通过 |
| 02 | `policy-first` | 6–10s | 先写发布政策，再写脚本。你要拦的是绝对质量不达标，还是相对已批准基线的回退？两者可以组合。 | 政策文档先于代码出现，两个阻断方向汇入同一门禁 | 先定义发布政策，再写门禁代码 |
| 03 | `required-set` | 6–10s | 必需 case 是硬门槛。任何一条失败都要阻断，除非修复，或者经审核把它移出必需集合。 | 必需 case 集合逐条过门，失败项锁死发布出口 | 必需 case 失败，就阻断发布 |
| 04 | `no-regression` | 6–10s | 防回退保护已经通过的 case。基线通过、候选失败，就触发阻断；原本失败的样本改善，不该被误拦。 | 基线与候选状态矩阵，Pass→Fail 红色阻断，Fail→Pass 放行审查 | 已通过项回退，必须触发阻断 |
| 05 | `stable-case-id` | 6–10s | 每条 case 要有稳定且唯一的 ID。否则基线和候选对不上，所谓新增失败和修复都可能是错配。 | 两次 run 按稳定 case ID 对齐，重复 ID 和错配高亮 | 先对齐 case ID，再比较结果 |
| 06 | `fail-closed` | 6–10s | 缺 case、重复 ID、任务报错、评分缺失或无效，一律让门禁失败。证据不完整时，不能默认放行。 | 五类不完整证据进入 fail-closed 闸门，没有转为 Pass | 缺失、报错、无效评分都阻断 |
| 07 | `approved-baseline` | 6–10s | 基线要是明确审核并批准的 run。把基线 artifact、Dataset 版本和评估器版本留在仓库，别自动选最新。 | 已批准基线卡与仓库 artifact 绑定，latest 指针断开 | 基线要批准，版本标识要入仓库 |
| 08 | `baseline-change` | 6–10s | 如果输入、期望输出、必需集合或评估器定义变了，先审查并更新基线。只重算候选，比较没有共同尺度。 | 四类变更触发基线复审，双边重算而非单边刷新 | 测试或评估定义变了，先复审基线 |
| 09 | `version-pin` | 6–10s | CI 里固定 Dataset 版本时间戳、应用 commit、Prompt 或模型版本和 SDK 版本。默认 latest 不利于复现。 | 五枚版本锁定钉住 CI 配置，latest 默认项被显式替换 | 固定数据、应用和 SDK 版本 |
| 10 | `action-pin` | 6–10s | GitHub Action 也要固定到明确 release。别让上游动作更新，悄悄改变你的发布门行为。 | Action release 标签锁定，浮动的未固定引用被打叉 | Action 固定 release，避免行为漂移 |
| 11 | `secrets-permissions` | 6–10s | Langfuse key 放 GitHub Secrets，工作流权限按需要给。画面只显示变量名，绝不展示真实密钥。 | Secrets 变量名与最小权限清单并列，所有值均遮罩 | 密钥入 Secrets，权限按需要给 |
| 12 | `runner-context` | 6–10s | Action 的 context 负责初始化客户端、加载指定 Dataset，并附加 commit 等 CI metadata。实验脚本用 context 启动 run。 | context 中央连接客户端、Dataset、CI metadata 和实验脚本 | 用 context 启动带 CI 元数据的实验 |
| 13 | `regression-error` | 6–10s | 分数越过发布阈值时，在实验代码里抛出 RegressionError，并附上 result。Action 才能带出指标和比较信息。 | 阈值越界触发 RegressionError，result 随错误进入 Action | 越过阈值，抛出 RegressionError |
| 14 | `script-error` | 6–10s | 回归和脚本崩溃都要让 CI 失败。不要为了变绿，关掉回归失败或脚本错误的阻断开关。 | 两类错误分别连接 CI Fail，两个关闭开关的操作被打叉 | 回归与脚本错误，都不能放行 |
| 15 | `result-json` | 6–10s | Action 的 result_json 保存标准化结果，failed 表示是否有回归或脚本错误。PR 评论只是展示，结构化输出还要留存。 | result_json 与 failed 输出进入存储，PR 评论作为单独展示层 | PR 评论之外，保留结构化结果输出 |
| 16 | `evidence-artifact` | 6–10s | 把 result_json、run 关联、Dataset 版本、基线标识和 commit 作为构建 artifact 保存。失败后能复查，而不是只看绿灯。 | 五项证据打包成构建 artifact，失败记录可重新打开 | 把门禁结果保存成可复查 artifact |
| 17 | `known-failure` | 6–10s | 已知失败要明确记录接受理由和负责人。不能因为它一直失败，就从必需集合里悄悄删掉。 | 已知失败登记卡含理由与负责人，静默删除被阻止 | 已知失败要审查，不能悄悄删除 |
| 18 | `combined-policy` | 6–10s | 实用门禁可以组合：必需 case 必过、已批准通过项不回退、汇总指标过线、不完整结果阻断。 | 四条政策形成组合锁，任一阻断都保持门关闭 | 必需项、回退、汇总、完整性组合把关 |
| 19 | `stamp` | 6–10s | 本集只是 prototype、L1 设计稿，没有运行 GitHub Action、Langfuse Experiment 或真实发布门。绿色示意图不是 CI 证据。 | PROTOTYPE / L1 印章，Action、Experiment、发布门均标未运行 | prototype / L1：不是 CI 已通过证据 |
| 20 | `cta` | 6–10s | 下一集回到评分本身：模型评审怎样用人工样本校准，避免门禁很严格，评估器却一直判错。 | LF-26 预告：人工样本 → 评审校准 → 分歧复核 → 门禁 | 下一集：先校准评估器，再相信门禁 |

## 固定构图顺序

`hook → policy-first → required-set → no-regression → stable-case-id → fail-closed → approved-baseline → baseline-change → version-pin → action-pin → secrets-permissions → runner-context → regression-error → script-error → result-json → evidence-artifact → known-failure → combined-policy → stamp → cta`

## 字幕与旁白

- 声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`，禁止整段变速。
- 首次出现中英并读：CI 持续集成、Experiment 实验、case 测试样本、run 运行、Dataset 数据集、metadata 元数据、artifact 构建证据包。
- 烧录字幕使用表中短句；SRT、VTT 使用同一时间轴，最后一条与片尾对齐。
- 不编造真实 CI 状态、run ID、阈值通过率、发布结果或模型质量结论。

## 演示与证据边界

1. 发布政策先于脚本：必需 case 必过与已批准通过项不回退可以组合，已知失败必须显式审查。
2. 缺失 case、重复 ID、任务失败、评分缺失或无效必须阻断；稳定 case ID 是跨 run 比较的前提。
3. 基线 artifact 与版本标识入库；数据、必需集合或评估器变化后，先复审基线再比较。
4. 固定 Dataset、应用、SDK 和 Action 版本；保留 `result_json` 与关联证据，PR 评论或绿色状态不单独构成证明。
5. 当前文件只定义概念课画面，不证明 GitHub Action、Langfuse Experiment 或真实发布门已运行。

## 官方来源（2026-11-23 已读取，录制当天仍需复核）

- Experiments in CI/CD：https://langfuse.com/docs/evaluation/experiments/experiments-ci-cd
- Compare experiments：https://langfuse.com/docs/evaluation/experiments/compare-experiments
- Experiments via SDK：https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk
- Datasets：https://langfuse.com/docs/evaluation/experiments/datasets
