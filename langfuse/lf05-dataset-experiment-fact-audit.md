# LF-05 事实审计：Dataset 与可重复实验

任务：LF05-S1。官方文档核对日期：2026-11-23（Asia/Shanghai）；本集为概念课程，当前无项目 key，未执行真实运行。

## 结论

这集要守住一句话：**固定 Dataset、版本和评分条件，用同一 Dataset 比较 Prompt/模型，保存失败样本；可重复指的是条件冻结，不是样本有业务代表性。**

- Dataset 是固定输入集合；run 是某次执行身份；item 有稳定 ID。
- 同一 Dataset、只改一个变量，才能谈比较；平均分不证明模型全面更好。
- 当前无项目 key，Dataset 创建、run、Score 写入、回读全部 BLOCKED。状态保持 `prototype / L1`。

## Dataset / item 字段（官方 experiments 数据模型，2026-11-23 读取）

来源：<https://langfuse.com/docs/evaluation/experiments/data-model>

| 对象 | 关键字段 | 边界 |
|---|---|---|
| Dataset | 一组 DatasetItem | 集合本身不代表业务代表性 |
| DatasetItem | `id`（项目级唯一、跨 dataset 不复用）、`datasetId`、`input`、`expectedOutput`、`metadata`、`sourceTraceId`、`sourceObservationId` | item 按 id upsert |
| DatasetRun | 一次执行身份 | 创建走 SDK/UI/OTEL |
| DatasetRunItem | run 与 item 的关联 | 读取走 Experiments API |

## run 读写路径

- 创建 run：Experiments via SDK / via UI / via OpenTelemetry。
- 读取 run、item、score：Experiments API。
- 没有用于创建新 experiment run 的公开 REST 端点；旧 `POST /api/public/dataset-run-items` 已废弃。
- v4 迁移：dataset runs → `/api/public/experiments`，`/dataset-run-items` → `/experiment-items`。

## 可重复的边界

“可重复”只针对冻结的 Dataset、版本、模型、参数和评分条件。比较必须明确比较组和唯一变量，不能用一条漂亮样例替代分组结果。成本、延迟、质量、稳定性数字必须来自同一轮可回读证据。

## 与现有 LF-05 审计的对齐

`lf05-fact-audit.md` 已覆盖概念、逐项边界、最小证据包。本文件补上官方 item 字段和 run 读写路径。旧文件里“即”有一处乱码，建议后续修正。当前实例的 health/readiness、历史 Trace、OTEL 认证门都不能替代 Dataset run、Score 写入和实验回读。

## 与其他 agent 的冲突

- 若有人把单次写入 2xx 升级成实验回读或业务结论，与本审计冲突。
- 若有人把平均分写成模型更好/总体满意/统计显著，与本审计冲突。
- 若有人用旧 `POST /api/public/dataset-run-items` 创建 run，与官方“已废弃”冲突。

## 需要冻结的字段

- 状态：`prototype / L1`；Dataset run、Score write、readback `BLOCKED`。
- item 字段：id、datasetId、input、expectedOutput、metadata、sourceTraceId。
- run 创建走 SDK/UI/OTEL；读取走 Experiments API。
- 禁出现：内网地址、真实 key / secret、Authorization 值、登录信息、PII。

## 依据

官方页面，2026-11-23 以 Markdown 端点读取：

- Experiments 数据模型：<https://langfuse.com/docs/evaluation/experiments/data-model>
- 比较实验：<https://langfuse.com/docs/evaluation/experiments/compare-experiments>
- v4 API 迁移映射：<https://langfuse.com/llms.txt>

仓库内证据：

- `langfuse/lf05-fact-audit.md`
- `langfuse/lf05-dataset-lesson.md`
- `langfuse/lf21-dataset-score-readback-fact-audit.md`

## 产物与验证

独占产物：本文件。未改视频、字幕、播放器、manifest 或 `docs/quality/00-project-state.md`，未 git commit。

## 风险、缺口与未完成

- 没有项目 key，Dataset run、Score 写入、回读全部未验证。
- 可重复不等于业务代表性。

## 建议下一步

由主 agent 把 LF-05 口播补上 item 字段和 run 读写路径。等级升级只能等受保护 run、Score 写入与同一 run 回读证据。
