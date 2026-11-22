# LF-07 事实审计：成本、token usage 和延迟

任务：LF07-S1。官方文档核对日期：2026-11-23（Asia/Shanghai）；本集为概念课程，当前无项目 key，未执行真实运行。

## 结论

这集要守住一句话：**在一次 Generation 里找到模型、token usage、耗时和成本字段，缺字段写 unknown；先看原始字段，再谈成本优化。一次本地 Trace 不能推出长期平均延迟、成本或模型整体效率。**

- usage 按 usage type 记录；cost 按 USD/usage type。
- 成本依赖 usage 完整性、provider、价格配置和计价时间。
- 对照实验固定输入、模型、参数、网络和样本。状态保持 `prototype / L1`。

## usage 与 cost 字段（官方，2026-11-23 读取）

来源：<https://langfuse.com/docs/observability/features/token-and-cost-tracking>

| 项 | 官方口径 | 边界 |
|---|---|---|
| usage details | 每个 usage type 消耗的单位数（input/output，及 provider 特定的 cached_tokens、audio_tokens 等） | 缺字段不能自行估算 |
| cost details | 每个 usage type 的 USD 成本 | 没有价格配置不能给金额 |
| 记录位置 | `generation` 和 `embedding` 类型的 observation | 其他类型不自动带 |
| usage | 必须 ingest | — |
| cost | 可 ingest，或按模型价格配置计算 | 价格表快照不等于本次实际费用 |

Langfuse 自带 OpenAI/Anthropic/Google 等热门模型价格，多数集成自动捕获 usage/cost；也可自建模型。

## 延迟与对照

- 同一事件的时间戳可算一次调用耗时，必须说明口径和时区。
- 一次调用不能推出 P95、稳定性、SLA 或“模型慢”。
- 对照固定输入、参数、模型、网络和样本，保存两次 run ID 与原始响应摘要。

## 与现有 LF-07 审计的对齐

`lf07-fact-audit.md` 已覆盖 model/usage/latency/cost 的可讲范围、最小证据包、发布门。本文件补上官方 usage/cost 按 usage type 记录、cost 可 ingest 或按价格计算、记录位置为 generation/embedding。旧文件里“复”有乱码，建议后续修正。

## 与其他 agent 的冲突

- 若有人缺字段时自行估算，或没有价格配置就给金额，与本审计冲突。
- 若有人用一次调用推出长期延迟/成本/模型效率，与本审计冲突。
- 若有人把价格表快照当本次实际费用，与本审计冲突。

## 需要冻结的字段

- 状态：`prototype / L1`；真实 Generation JSON、usage、cost 回读 `BLOCKED`。
- usage 按 usage type；cost USD/usage type；usage 必 ingest，cost 可 ingest 或计算。
- 缺字段写 unknown。
- 禁出现：内网地址、真实 key / secret、Authorization 值、登录信息、PII。

## 依据

官方页面，2026-11-23 以 Markdown 端点读取：

- Token & Cost Tracking：<https://langfuse.com/docs/observability/features/token-and-cost-tracking>

仓库内证据：

- `langfuse/lf07-fact-audit.md`
- `langfuse/lf07-cost-latency-lesson.md`
- `langfuse/evidence-pack-lf06-10.md`

## 产物与验证

独占产物：本文件。未改视频、字幕、播放器、manifest 或 `docs/quality/00-project-state.md`，未 git commit。

## 风险、缺口与未完成

- 没有项目 key，真实 usage/cost/latency 回读全部未验证。
- 示意数字必须标为示意。

## 建议下一步

由主 agent 把 LF-07 口播补上 usage/cost 按 usage type 记录和 cost 两种来源。等级升级只能等受保护运行与同一 Generation 回读证据。
