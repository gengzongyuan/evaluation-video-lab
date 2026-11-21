# LF-21｜Dataset Run、Score 写入与实验回读

## 一句话结果

看完后，观众能把一组固定 Dataset 交给一次可追溯的 evaluation run，用 Score 记录每条结果，再用同一个 run 标识回读样本、汇总和失败原因；没有真实凭据时，知道哪些步骤只能停在 `BLOCKED`。

## 适合谁

已经理解 Trace、Dataset 和实验比较，希望把“模型回答好不好”变成可复查记录的评测工程师、开发者和 QA。

## 180 秒时间轴

| 时间 | 口播 | 画面/动作 | 证据标签 |
|---|---|---|---|
| 0:00–0:15 | “今天不先看平均分。先冻结 Dataset、版本和评分规则，再创建一轮 run。” | 标题卡：Dataset → Run → Score → Readback；右下角 `prototype / L1` | 概念 |
| 0:15–0:38 | “Dataset 是固定输入集合；run 是这一次模型或 Prompt 版本在集合上的执行身份。没有 run ID，之后的分数很难追到具体输入。” | 四行卡片：dataset name/version、run ID、prompt/model version、timestamp | 官方概念，待复核 |
| 0:38–1:02 | “第一步冻结条件：Dataset 版本、模型和参数、Prompt label、评估器版本、运行时间。任何一项变化都要产生新 run，而不是覆盖旧结果。” | 在表格中勾选五个冻结字段；展示 `run-A` 与 `run-B` | 方法建议 |
| 1:02–1:28 | “第二步执行每个样本，并把结果和样本 ID 绑定。输出可以是答案，也可以是失败状态；失败不能被静默丢弃。” | 示意 JSON：`item_id`、`run_id`、`output`、`status`；敏感字段打码 | 示意代码，不是实测 |
| 1:28–1:52 | “第三步写 Score。Score 必须带分数名、数值或分类值、来源和关联对象。自动评分、人工评分和规则评分要分开，否则汇总会混成一个数字。” | 三色标签：`judge`、`human`、`rule`；显示 `score=0.8` 仅作示意 | 口径要求 |
| 1:52–2:15 | “第四步回读。先按 run ID 找到这轮结果，再逐条检查输入、输出、Score、错误和时间戳，最后才看总体分。” | 回读清单逐项亮起；右侧标注 `readback pair` | 证据闭环 |
| 2:15–2:37 | “比较两个 Prompt 时，Dataset、评分规则和统计口径必须相同。平均分只能描述这组样本，不能直接说模型全面更好。” | `run-A` / `run-B` 并排；下方显示失败样本和分组汇总 | 结论边界 |
| 2:37–2:55 | “本集的最小验收是：有 run ID、有原始输出、有 Score、有回读响应、有版本和时间。缺任何一个，就停在 BLOCKED。” | 红色门禁卡：ID、output、score、readback、version/time | 发布门禁 |
| 2:55–3:00 | “下一集继续看 Score 如何进入失败样本和回归。” | CTA：保存本集，复查你的证据包 | 课程衔接 |

## 演示步骤（录制时执行）

1. 记录本次运行的 `run_id`、Dataset 名称/版本、Prompt label、模型/SDK 版本和时间。
2. 选择至少两个脱敏 Dataset item，展示固定的 `item_id`，不要展示完整用户输入、密钥或内网地址。
3. 使用当前官方支持的 SDK 或 Langfuse evaluation/experiment 入口创建 run；保存脱敏请求摘要、HTTP 状态和非敏感响应。
4. 对每个 item 写入一个明确来源的 Score，例如 `correctness`，并记录数值范围、评估器版本和关联 run/item。
5. 用当前版本支持的 UI/API 按 `run_id` 回读同一批结果；保存脱敏 JSON 或截图，并核对 item、output、score、错误和时间戳。
6. 只有写入和回读都对应同一轮新 run，才把课程证据从 `prototype / L1` 申请升级；否则画面固定标注 `BLOCKED`。

## 最小证据包

- `run-metadata.json`：run ID、Dataset 版本、Prompt/model/SDK 版本、实例版本、时间和运行 commit。
- `payload.redacted.json`：脱敏输入和输出摘要，不包含 key、secret、PII 或完整 prompt。
- `write-response.json`：HTTP 状态、非敏感响应和时间，不保存 Authorization。
- `score-records.redacted.json`：item ID、score 名称/值、来源、评估器版本和关联 ID。
- `readback.redacted.json` 或脱敏 UI 截图：同一 run ID 的结果回读。
- `claim-review.md` 与 `SHA256SUMS.txt`：逐字段断言审阅和文件完整性。

## 当前环境边界

当前 Langfuse 4.79.0 实例可以证明 health/readiness 的时间点采样、旧 API 的 `events_only` 迁移信号和 OTEL 入口认证门；当前 shell 没有项目 Public/Secret Key。因此本集不能声称 Dataset run、Score 写入、实验汇总或回读已经在当前实例成功完成。对应状态保持：

- Dataset run：`BLOCKED`
- Score write：`BLOCKED`
- Run/Score readback：`BLOCKED`
- 实验比较结论：`BLOCKED`

历史截图、示意 JSON、空 POST 的 401 或健康检查 200 都不能替代本集同一 run 的写入与回读证据。

## 官方来源（录制前复核）

- <https://langfuse.com/docs/evaluation/overview>
- <https://langfuse.com/docs/evaluation/experiments>
- <https://langfuse.com/docs/evaluation/evaluation-methods>
- <https://langfuse.com/docs/scores>
- <https://langfuse.com/docs/datasets>

录制当天重新核对页面、SDK 版本和 v4 events-only 支持方式；若链接、字段或入口变化，先修订脚本再录制。

## 发布前检查

- [ ] 约 180 秒，音频和视频流均存在（若生成原型，明确标为 prototype）。
- [ ] 字幕逐字复核 `Dataset`、`run_id`、`Score`、`readback` 和 `BLOCKED`。
- [ ] UI/API、输入输出、Trace/Run ID、Prompt、key、secret、PII 和内网地址均已脱敏。
- [ ] 结论只覆盖本轮 Dataset、评分规则和运行条件，不写成全面模型排名。
- [ ] 真实运行证据包含同一 run 的写入响应、Score 记录、回读响应、版本和时间戳。

## 参考资产

- `langfuse/lf05-dataset-lesson.md`
- `langfuse/lf06-score-lesson.md`
- `langfuse/lf11-experiment-compare-lesson.md`
- `langfuse/evidence/lab02-readiness-contract-2026-11-22.md`
- `langfuse/evidence/lf19-evidence-audit-2026-11-22.md`
