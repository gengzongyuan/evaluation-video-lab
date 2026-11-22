# LF-06 事实审计：Evaluation、Score 与失败样本

任务：LF06-S1。官方文档核对日期：2026-11-23（Asia/Shanghai）；本集为概念课程，当前无项目 key，未执行真实运行。

## 结论

这集要守住一句话：**把人工、代码或模型评分绑定到运行证据，保留失败样本供复核。Score 是判断工具，不是脱离任务的真理；高分不能掩盖关键失败。**

- 评分前先定义问题、范围、单位、空值和失败判定。
- Score 关联固定 Trace/Observation/Dataset run，保留关联 ID 和 evaluator 版本。
- 高分低分都要抽查，比较时保留样本量、失败类型和版本。状态保持 `prototype / L1`。

## Score 数据模型（官方，2026-11-23 读取）

来源：<https://langfuse.com/docs/evaluation/scores/data-model>

| 字段 | 含义 |
|---|---|
| `name` | 分数名，如 correctness |
| `value` | 数值；numeric/boolean 必有，categorical 可选，text 不用 |
| `stringValue` | 字符串值；categorical/boolean/text 用 |
| `source` | 来源，只有 `API` / `EVAL` / `ANNOTATION` 三种，自动设置 |
| `traceId` | 关联 trace；也可关联 observation/session/datasetRun |
| `comment` | 评估说明 |

分数类型分 numeric、categorical、boolean、text。人工、代码、模型评分要分开，否则汇总会混成一个数字。

## 高低分与失败样本

- 对照总分、样本量、失败类型和原始输入输出，抽查高分和低分。
- 只看平均分不能得出模型更好、稳定或上线结论。
- 总分 90 的示意画面必须标为示意，不得使用未验证的真实项目数据。
- 固定数据、模型、Prompt、评分规则和版本后比较，并保留失败样本。

## 读写路径

- 写：新代码用 `POST /api/public/scores`。
- 读：`/api/public/v3/scores`。
- 回读用同一关联 ID 核对 Score 与原始输入输出。

## 与现有 LF-06 审计的对齐

`lf06-fact-audit.md` 已覆盖可讲/不可讲、最小证据包、发布门禁。本文件补上官方 Score 来源三值、类型和当前读写路径。旧文件里“单”和“证”有乱码，且引用了过时路径 `/docs/observability/features/scores`，建议后续修正为 `/docs/evaluation/scores/...`。

## 与其他 agent 的冲突

- 若有人把“Score 记录成功”说成“模型质量已证明”，与本审计冲突。
- 若有人用“更好/更稳定/提升百分比”而无同条件数据，与本审计冲突。
- 若有人沿用旧 `/docs/observability/features/scores` 作来源，以本文件当前路径为准。

## 需要冻结的字段

- 状态：`prototype / L1`；Score write/readback、Dataset run、比较 `BLOCKED`。
- Score 来源：API / EVAL / ANNOTATION；类型 numeric/categorical/boolean/text。
- 写 `/api/public/scores`，读 `/api/public/v3/scores`。
- 禁出现：内网地址、真实 key / secret、Authorization 值、登录信息、PII。

## 依据

官方页面，2026-11-23 以 Markdown 端点读取：

- Scores 数据模型：<https://langfuse.com/docs/evaluation/scores/data-model>
- v4 API 迁移映射：<https://langfuse.com/llms.txt>

仓库内证据：

- `langfuse/lf06-fact-audit.md`
- `langfuse/lf06-score-lesson.md`
- `langfuse/evidence-pack-lf06-10.md`

## 产物与验证

独占产物：本文件。未改视频、字幕、播放器、manifest 或 `docs/quality/00-project-state.md`，未 git commit。

## 风险、缺口与未完成

- 没有项目 key，真实 Score 写入、回读、Dataset run、比较全部未验证。
- 平均分不能掩盖关键失败。

## 建议下一步

由主 agent 把 LF-06 口播补上 Score 来源三值和读写路径，替换过时来源路径。等级升级只能等受保护 Score 写入与同一关联 ID 回读证据。
