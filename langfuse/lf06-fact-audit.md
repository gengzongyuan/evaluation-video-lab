# LF-06｜Evaluation、Score 与失败样本事实审计

核对日期：2026-11-22（Asia/Shanghai）

## 结论

LF-06 可以作为 `prototype / L1` 快切课程继续制作。官方文档可以支持“Score 是绑定到运行证据的评价结果”“评分需要定义规则、范围、单位并保留 evaluator 版本”“高分不能掩盖关键失败”等教学表达。当前实例没有安全注入项目 key，本轮没有真实 Score 写入、Dataset run、Trace/Observation 回读或 UI/API 字段核验，因此所有运行性表述必须保持 `BLOCKED`。

## 可讲与不可讲

| 主题 | 当前可讲 | 当前不能讲 |
|---|---|---|
| 评分规则 | 先定义问题、范围、单���、空值和失败判定，再写入 Score | 某个规则一定代表业务质量，或适用于所有任务 |
| 评分对象 | Score 应关联固定 Trace、Observation 或 Dataset run，并保留关联 ID | 当前项目已经成功绑定了某条新 Trace 或 run |
| Score 字段 | 录制前按官方当前页面核对 `score_id`、数值/数据类型、关联 ID、evaluator 版本和时间 | 未经当前版本回读证明的具体参数名、响应结构或 UI 位置 |
| 高低分样本 | 对照总分、样本量、失败类型和原始输入输出，抽查高分和低分 | 只看平均分就能得出模型更好、稳定或上线结论 |
| 评测回归 | 固定数据、模型、Prompt、评分规则和版本后比较，并保留失败样本 | 一次运行或单个漂亮样例证明长期提升 |

## 录制前最小证据包

1. 官方当前 Evaluation/Score 页面 URL、核对日期和页面版本信息。
2. 受保护环境中的 SDK、Langfuse 实例版本、运行 commit 和项目凭据来源；仓库不得保存 key、secret 或 Authorization header。
3. 脱敏的固定 Trace 或 Dataset run 标识，以及评分规则、单位、空值规则和 evaluator 版本。
4. Score 写入请求的脱敏摘要、HTTP/SDK 响应和写入时间；仅有 `2xx` 只能说明观察到响应，不能单独证��回读成功。
5. 用同一关联 ID 回读 Score 与原始输入输出，保存脱敏 JSON/UI 证据，核对值、类型、关联关系和时间戳。
6. 高分、低分和失败样本各至少一条，保留样本量、分组条件和失败类型；生成 SHA-256 清单。

## 当前状态

- 官方来源入口：`https://langfuse.com/docs/evaluation/overview`、`https://langfuse.com/docs/observability/features/scores`，录制当天必须重新核对。
- 当前项目 key：缺失；不执行真实 Score 写入或回读。
- `Score write`：`BLOCKED`。
- `Score readback`：`BLOCKED`。
- `Dataset run / experiment comparison`：`BLOCKED`。
- 课程状态：`prototype / L1`。

## 发布门禁

- 字幕和旁白不得把“Score 记录成功”说成“模型质量已证明”。
- 任何“更好、更稳定、更准确、提升百分比”必须有同条件数据、样本量、失败样本和版本追溯；否则改成“本次观察”或删除。
- 总分 90 的示意画面必须标为示意，不得使用未验证的真实项目数据。
- 没有同一关联 ID 的写入和回读证据，保持 `BLOCKED`，不得升级为 verified。

## 依据

- `langfuse/lf06-score-lesson.md`
- `langfuse/evidence-pack-lf06-10.md`
- `langfuse/source-verification.md`
- `langfuse/docs/quality/` 中的 LAB-02 环境与 readiness 契约

