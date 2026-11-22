# LF-15 事实审计：视频与实验发布门禁

任务：LF15-S1。官方文档核对日期：2026-11-22（Asia/Shanghai）。
独占产物：本文件。未改视频、字幕、播放器、manifest 或 docs/quality/00-project-state.md。

## 结论

LF-15 要讲的不是怎么点发布，而是两类不能混用的门禁。

1. 课程视频发布门：脚本、成片、原始素材、脱敏、manifest 和回滚是否一致。媒体可播放不等于证据已验证。
2. Langfuse 实验/变更发布门：同一 Dataset 版本、同一评估器定义、可回读的 run/Score、以及明确的通过或失败政策。平均分、UI 截图、health/readiness 都不能单独放行。

官方产品支持 Dataset、Experiments、Scores、Prompt versions/labels，以及 CI 中用实验结果拦截回归。当前仓库没有受保护项目 key，没有 Dataset run、Score 写入、实验比较或 Prompt production 标签切换的运行证据。因此本集必须保持 prototype / L1，不能声称当前实例、当前 Prompt 或当前模型已经通过发布。

## 我的理解

仓库里的 LF-15 脚本只有 17 行，把断言可回指、脱敏、版本追溯、回滚、blocked 条件写成制作清单。这是课程质量控制，不是 Langfuse 自动证明应用正确。

课程地图里编号 15 的官方依据是 Prompt 比较实验；manifest 的 LF-15 标题是视频与实验发布门禁。本集应同时覆盖：如何用 Langfuse 实验结果做变更门禁；如何用本系列自己的证据等级决定视频能不能对外讲。两者共享同一原则：没有同一对象的写入与回读，就停在 BLOCKED。

## 隐含假设

- 2026-11-22 读取的官方 Markdown 文档反映当天公开口径；字段名、入口和 GitHub Action 参数会变，录制前必须重读。
- 历史材料中的 server 4.79.0 与 health/readiness 观察是时间点采样，不是本任务重新验证。
- 内部 check_video_quality.py 只检查媒体；它不是 Langfuse 实验门。

## 官方能力与可讲述范围

| 主题 | 官方支持的口径 | 不能由此推出 |
|---|---|---|
| Dataset | Dataset 是项目内唯一名称的输入和期望输出集合；UI、SDK、OpenTelemetry 实验都可以使用 | 建了 Dataset 就等于实验已跑完，或样本代表全部真实流量 |
| Dataset version | 实验可指定历史 Dataset 版本；未指定则用最新版。版本固定的是测试数据 | 版本固定后模型输出确定，或两次 run 必然可复现 |
| Experiments via UI | 可在 UI 对 Prompt 版本或模型跑 Prompt Experiments，并可选用 LLM-as-a-Judge 或 code evaluator | 点了 Run Experiment 就证明结果已回读、评估器可靠、可上线 |
| Experiments via SDK | 可用本地数据或 Langfuse Dataset 跑实验；支持 item/run 级评估、并发和错误隔离；官方建议用 experiment runner | 一次 SDK 调用等于生产验收；旧 SDK 的 dataset run helper 仍可用。当前 Python v5 / JS v6 已移除旧 helper |
| Scores | Score 是评价结果的通用对象，可挂到 Trace、Observation、Session 或 Dataset run；有 NUMERIC、分类、布尔等类型 | 有一个分数就代表质量全面更好；空值或失败评估可当通过 |
| 比较实验 | 先看汇总，再看变差的 case 并打开 Trace。发布决策应使用同一 Dataset 版本和同一评估器定义，并记录应用 commit、Prompt/模型版本、评估器版本 | 平均分相同或更高就可以发布；缺失 case 算通过 |
| CI 发布政策 | 官方给出两类政策：所有 required case 必须通过；已批准通过的 case 不得回退。可组合。缺失 case、重复 ID、任务失败、评估器无结果必须失败。失败 run 不会因为是最新一次就变成批准基线 | 接上 GitHub Action 就等于当前仓库已经有门禁；安装 latest SDK 即锁定版本 |
| Prompt 发布 | Prompt 用 version 和 label 管理；把 production 或环境 label 赋给某个版本即部署该版本 | 贴上 production 就证明质量、延迟、成本和安全已验收 |
| 视频/课程门 | 本系列自制：断言回指来源或运行记录、脱敏、版本、回滚、失败不得剪成成功 | 媒体门 PASS、页面能打开或 health 200 等于 Langfuse 实验通过 |

官方明确提醒：平均质量提升可以掩盖关键 case 回归。比较视图里两个 run 都可能是 50% 准确率，平均值不能回答能不能发布。

## 三层证据，禁止互相替代

| 层 | 能证明 | 不能证明 |
|---|---|---|
| health / readiness | 对应端点在采样时刻有响应 | 新 Trace、Dataset run、Score、Worker 消费、对象存储、权限或生产安全 |
| UI 截图 / 示意表 | 当时界面长什么样，或课程想讲的结构 | 当前实例写入成功、ID 可回读、评估器版本未变、结果属于同一 run |
| 写入 + 回读 | 在固定版本下，同一 Dataset/run/item/Score ID 可从请求对到响应 | 统计显著、业务因果、全部用户满意、可无条件上线 |

发布视频时如果只用第一层或第二层，口播必须说 prototype / L1。只有第三层齐全，才可申请把那一条运行断言升到 verified / L2。整集课程是否对外发布，还要过脱敏、回滚和字幕一致性。

## 建议冻结字段

实验门缺一不可，否则 BLOCKED：Dataset 名称与 version；稳定 item/case ID，缺失 case 不得计为 pass；Prompt name、version、label；模型、参数、应用 commit；Experiment 或 dataset run ID 与时间戳；Evaluator 或 score 名称、数据源（human / code / LLM-as-a-Judge）、版本；被明确批准的基线 run ID，而不是最新一次；发布政策 required-pass 或 no-regression 或两者组合；回读响应中同一 run 的 item 输出、Score、错误、时间。

视频门与实验门分开记录：脚本、成片、原始素材、SRT/VTT、manifest 指向同一 git commit；脱敏检查无项目 key、secret、Authorization、内网地址、登录信息、PII、完整未脱敏 prompt；每条画面断言的证据等级为 L1 示意、L2 回读或 blocked；回滚引用上一个可播放 commit；媒体检查结果不得写成 Langfuse 验证结果。

## 当前实例与不可证明范围

本任务没有安全项目 Public/Secret Key，没有创建 Dataset、运行 Experiment、写入 Score、比较 run，也没有给 Prompt 打 production 标签。因此 Dataset run、Score 写入、实验回读、CI RegressionError、Prompt 部署全部保持 BLOCKED。health/readiness、旧 API 的 events_only 提示、OTEL 入口存在、空 POST 401、Dashboard 历史截图，都不能当作本集发布证据。不得把版本存在、平均分更高、一次实验、Action 仓库存在说成当前变更可上线。

## 对旧 LF-15 脚本的修订

- 保留：断言要有来源或运行记录；输入输出和 ID 要脱敏；版本、日期、SDK、服务端、commit 要记录；失败和缺字段不得剪成成功；成片与脚本可回滚。
- 增加：先分开视频门和实验门，再讲它们如何共用 ID 回读原则。
- 增加：官方 CI 政策与比较实验的平均值会掩盖回归；用示意表，不填当前实例数字。
- 增加：Prompt production label 是部署指针，不是评测通过证明。
- 收紧：发布门是质量控制，不是产品正确性自动证明。当前只能演示清单和失败条件，不能演示一次真实放行。

## 建议演示步骤（示意，未在本项目执行）

1. 出示两张门禁卡：左为视频门，右为实验门；标注 prototype / L1。
2. 列出实验冻结字段：Dataset version、Prompt version/label、evaluator version、baseline run。
3. 用官方比较实验的示意：两个 run 平均分相同，但关键 case 从 pass 变 fail，因此不能发布。
4. 展示 CI 政策：required case 必须过；已批准 pass 不得回退。缺失评估结果等于失败。
5. 对照视频门：即使旁白清楚、字幕齐全，只要没有同一 run 的回读，课程结论仍停在 L1。
6. 结尾 CTA：LF-21 才处理真实 Dataset run 与 Score 回读；本集不伪造 ID。

## 最小证据包（真实放行时才需要）

1. experiment-metadata.json：Dataset version、run IDs、Prompt/model/evaluator 版本、commit、时间。
2. baseline-approval.md：谁在何时批准该基线；失败 case 的明确接受记录。
3. item-results.redacted.json：稳定 case ID、输出摘要、Score、错误；敏感字段已删除。
4. readback.redacted.json 或脱敏 UI：按同一 run ID 回读。
5. video-gate.json：成片路径、字幕路径、脱敏结果、回滚 commit、媒体检查命令输出。
6. SHA256SUMS.txt 与逐条 claim review。

没有第 1 到 4 项时，实验相关口播只能讲方法和反例，不能讲已通过。

## 敏感信息规则

画面、字幕、审计文件不得出现内网地址或可定位主机；项目 key、secret、Authorization、cookie、登录后 URL；用户 PII、完整未脱敏 prompt/output；可复用的完整请求头。需要提到 key 时，只允许说：没有项目 key 时不能声称链路通过。

## 官方来源（2026-11-22 实际读取，Accept: text/markdown）

- Evaluation overview：https://langfuse.com/docs/evaluation/overview
- Evaluation core concepts：https://langfuse.com/docs/evaluation/core-concepts
- Datasets / experiments overview：https://langfuse.com/docs/evaluation/experiments/overview
- Experiments via SDK：https://langfuse.com/docs/evaluation/experiments/experiments-via-sdk
- Experiments via UI：https://langfuse.com/docs/evaluation/experiments/experiments-via-ui
- Compare experiments：https://langfuse.com/docs/evaluation/experiments/compare-experiments
- Experiments in CI/CD：https://langfuse.com/docs/evaluation/experiments/experiments-ci-cd
- Scores：https://langfuse.com/docs/observability/features/scores
- LLM-as-a-Judge：https://langfuse.com/docs/evaluation/evaluation-methods/overview
- Prompt version control：https://langfuse.com/docs/prompt-management/features/prompt-version-control

页面 HTTP 200 只证明当天文档可访问。GitHub Action langfuse/experiment-action 的存在不构成本仓库已配置门禁。

## 验证

见本任务执行的 test -s 与 UTF-8/敏感词检查。本审计只约束课程断言和证据边界，不替代受保护环境中的 Dataset run、Score 写入、实验比较和 Prompt 部署。

## 审计结论

LF-15 可以按先分清视频门和实验门，再讲官方比较与 CI 政策，最后强调无回读即 BLOCKED 来制作。官方能力有来源；当前实例运行证据缺失。状态保持 prototype / L1，不能升级成熟度，也不能把内部媒体门或 health 200 说成实验已放行。
