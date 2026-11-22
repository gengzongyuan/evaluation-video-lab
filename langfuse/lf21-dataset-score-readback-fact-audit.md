# LF-21 事实审计：Dataset run、Score 写入与实验回读

任务：LF21-S1。官方文档核对日期：2026-11-23（Asia/Shanghai）；本集为课程脚本，当前无项目 key，未执行真实运行。

## 结论

这集要守住一句话：**先冻结 Dataset、版本和评分规则，创建一轮可追溯的 run，用 Score 记录每条结果，再用同一个 run 标识回读；没有真实凭据时，run、Score 写入、回读、比较结论全部停在 BLOCKED。**

- Dataset 是固定输入集合；run 是某一次模型/Prompt 版本在集合上的执行身份；Score 记录每条结果。
- 回读必须回到同一 run 的样本、Score、错误和时间戳，最后才看汇总。
- 平均分只描述这组样本和这套口径，不能写成模型全面更好。
- 状态保持 `prototype / L1`。

## Score 数据模型（官方，2026-11-23 读取）

来源：<https://langfuse.com/docs/evaluation/scores/data-model>

| 字段 | 含义 | 边界 |
|---|---|---|
| `name` | 分数名，如 correctness | 不同类型分数要分开命名 |
| `value` | 数值；numeric/boolean 必有，categorical 可选，text 不用 | 不是所有分数都有数值 |
| `stringValue` | 字符串值；categorical/boolean/text 用 | — |
| `source` | 来源，只有 `API` / `EVAL` / `ANNOTATION` 三种，自动设置 | 自动评分、人工评分、API 写入不能混成一个数字 |
| `traceId` | 关联的 trace | 也可关联 observation/session/datasetRun |
| `comment` | 评估说明 | 常用于反馈或评估理由 |

分数类型分 numeric、categorical、boolean、text。汇总时不同类型不能混算。

## 实验 run 的读写路径（官方，2026-11-23 读取）

来源：<https://langfuse.com/docs/evaluation/experiments/data-model>

- 创建 run 的路径：Experiments via SDK、via UI、via OpenTelemetry。
- 读取 run、item、score：用 Experiments API。
- **没有用于创建新 experiment run 的公开 REST 端点**；旧 `POST /api/public/dataset-run-items` 已废弃。

v4 API 迁移映射（官方索引）：
- 读：dataset runs 与 `/dataset-run-items` → `/api/public/experiments` 与 `/experiment-items`；scores 读 → `/api/public/v3/scores`。
- 写：新代码用 `POST /api/public/scores`。

## 最小证据闭环

要把“跑了一次评测”升级成可复核证据，至少要留下同一轮新 run 的：

1. `run-metadata.json`：run ID、Dataset 版本、Prompt/model/SDK 版本、实例版本、时间、运行 commit。
2. `payload.redacted.json`：脱敏输入输出摘要。
3. `write-response.json`：HTTP 状态、非敏感响应、时间。
4. `score-records.redacted.json`：item ID、score 名称/值、来源、评估器版本、关联 ID。
5. `readback.redacted.json` 或脱敏 UI 截图：同一 run ID 的回读。
6. `claim-review.md` 与 `SHA256SUMS.txt`：逐字段审阅和完整性。

缺任何一个，结论停在 BLOCKED。

## 回读路径

- 用当前 v4 支持的 Experiments API / v3 scores 读取同一 run 的 item、output、score、错误、时间戳。
- 不用已废弃的 `POST /api/public/dataset-run-items` 创建 run。
- 逐条核对后再看汇总；失败样本不能被静默丢弃。

## 与现有 LF-21 课稿的对齐

`lf21-dataset-score-readback-lesson.md` 的方向与本审计一致：冻结条件 → 执行绑定样本 → 写 Score → 回读 → 比较边界。需要补强的两点：

- Score 来源要对齐官方三值 `API`/`EVAL`/`ANNOTATION`，课稿里的 `judge`/`human`/`rule` 是讲法，底层字段是这三类。
- 明确创建 run 走 SDK/UI/OTEL，读取走 Experiments API；不要暗示有一个公开的“创建 run REST 端点”。

## 与其他 agent 的冲突

- 若有人把平均分升高写成“模型更好/总体满意/统计显著”，与本审计冲突。
- 若有人用旧 `POST /api/public/dataset-run-items` 创建 run，与官方“已废弃”冲突。
- 若有人把 health 200、OTEL 401、历史截图当成本集 run/Score 已写入，与本审计冲突。

## 需要冻结的字段

- 状态：`prototype / L1`；Dataset run、Score write、Run/Score readback、比较结论均 `BLOCKED`。
- Score 来源：API / EVAL / ANNOTATION；类型 numeric/categorical/boolean/text。
- run 创建走 SDK/UI/OTEL；回读走 Experiments API / v3 scores。
- 最小证据包六件齐全才申请升级。
- 禁出现：内网地址、真实 key / secret、Authorization 值、登录信息、PII、未脱敏 prompt。

## 依据

官方页面，2026-11-23 以 Markdown 端点读取：

- Scores 数据模型：<https://langfuse.com/docs/evaluation/scores/data-model>
- Experiments 数据模型：<https://langfuse.com/docs/evaluation/experiments/data-model>
- v4 API 迁移映射（官方索引）：<https://langfuse.com/llms.txt>

仓库内证据：

- `langfuse/lf21-dataset-score-readback-lesson.md`
- `langfuse/lf15-release-gate-fact-audit.md`
- `langfuse/lf05-fact-audit.md`

## 产物与验证

独占产物：本文件。未改视频、字幕、播放器、manifest 或 `docs/quality/00-project-state.md`，未 git commit。

## 风险、缺口与未完成

- 没有项目 key，Dataset run、Score 写入、回读、比较全部未验证。
- 本集只有课程脚本，尚无视频。
- 平均分/单次实验不能推出模型全面更好。

## 建议下一步

由主 agent 把 LF-21 口播补上官方 Score 来源三值和 run 读写路径。等级升级只能等受保护 run、Score 写入与同一 run 回读证据。
