# LF-05 Dataset 与可重复实验事实审计（2026-11-22）

## 审计结论

LF-05 可以制作成 `prototype / L1` 快切课程：官方页面支持讲 Dataset、固定 item、run 和实验比较的概念；当前仓库脚本已经把“同一 Dataset、只改一个变量、保存失败样本”作为演示主线。当前实例没有安全注入项目 key，因此 Dataset 创建、run 执行、Score 写入和结果回读全部保持 `BLOCKED`，不能把示意数据或历史截图说成当前运行结果。

## 来源核验

| 来源 | 当前 HTTP | 可支持的说法 | 不能支持的说法 |
|---|---:|---|---|
| https://langfuse.com/docs/datasets | 200 | Dataset、item 和可重复输入的官方概念入口；录制前需重看当前字段 | 当前项目已创建 Dataset、item ID 一定可回读、当前 UI 布局不变 |
| https://langfuse.com/docs/evaluation/experiments | 200 | 使用固定数据和条件比较实验的概念入口；需按当前页面核对 run/实验 API | 任一 Prompt/模型在业务上更好、某次平均分可泛化 |
| https://langfuse.com/docs/observability | 200 | 观测链路和运行记录的总览入口 | 当前实例已完成 Dataset run、Score 或成本/延迟回读 |

页面返回 200 只证明官方入口当前可访问；具体字段、SDK 参数和 UI 操作必须在录制当天重新核对。

## 逐项事实边界

| 课程断言 | 当前状态 | 放行口径 |
|---|---|---|
| 固定 item 可复用输入 | `docs-supported / concept` | 可以讲概念和脱敏示意，不声称当前项目已落库 |
| 每个 item 有稳定 ID、版本和来源 | `needs-runtime-review` | 录制前以当前 SDK/UI 返回字段为准，保存脱敏 JSON |
| Prompt v1 与 v2 可在同一 Dataset 上运行 | `needs-runtime-review` | 需要两个本轮 run 的 run ID、条件和 commit；没有 key 保持 BLOCKED |
| 结果可以附加 Score | `needs-runtime-review` | 需要保存 Score 写入响应、Score ID/名称和值及关联 run/item |
| 失败样本和分组结果支持比较 | `needs-runtime-review` | 需要保存原始失败样本摘要、分组规则和同一评分口径 |
| 平均分证明模型更好 | `forbidden` | 必须改成“本次条件下观察到的差异”，并同时展示失败样本、波动和条件 |

## 录制前最小证据包

在受保护环境执行，不把 key、secret、Authorization、PII 或完整业务输入输出写入仓库：

1. `run-metadata.json`：run ID、Dataset 名称/版本、item 数量、Langfuse/SDK/运行版本、commit 和时间。
2. `dataset-items.redacted.json`：稳定 item ID、脱敏输入、期望字段和来源摘要。
3. `run-v1.redacted.json`、`run-v2.redacted.json`：两次 run 的 Prompt/模型/参数、状态和关联 item ID。
4. `scores.redacted.json`：Score 名称、值、数据类型、关联 run/item 和写入响应。
5. `failures.redacted.json`：失败样本 ID、失败类别和必要的脱敏输出摘要。
6. `readback.redacted.json`：从当前版本支持的 UI/API 回读 Dataset、run、Score 和 item 关系。
7. `claim-review.md` 与 `SHA256SUMS.txt`：逐字段断言审阅、脱敏检查和证据完整性。

以上材料缺任何一项，LF-05 保持 `prototype / L1`；即���单次写入返回 2xx，也只能说明写入响应被观察到，不能自动升级为实验回读或业务结论。

## 视频脚本风险

- “可重复”只针对冻结的 Dataset、版本、模型、参数和评分条件，不代表样本具有业务代表性。
- “比较 Prompt/模型”必须明确比较组和唯一变量，不能用一条漂亮样例替代分组结果。
- 成本、延迟、质量和稳定性数字必须来自同一轮可回读证据；当前脚本只能讲方法和证据要求。
- 当前实例的 health/readiness、历史 Trace 或 OTEL 认证门探针不能替代 Dataset run、Score 写入和实验回读。

## 复核命令

```bash
test -s langfuse/lf05-dataset-lesson.md
python3 langfuse/validate_manifest.py
curl -L -s -o /dev/null -w '%{http_code}\n' https://langfuse.com/docs/datasets
curl -L -s -o /dev/null -w '%{http_code}\n' https://langfuse.com/docs/evaluation/experiments
```

本审计结论：官方概念入口可访问；当前运行证据缺失；LF-05 可继续制作快切原型，但不能宣称 Dataset run、Score 写入或实验回读已在本实例成功。
