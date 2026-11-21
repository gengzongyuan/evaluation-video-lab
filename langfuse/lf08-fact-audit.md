# LF-08 反馈回流 Score 事实与来源审计

核验日期：2026-11-22（Asia/Shanghai）

## 官方来源可证明范围

| 来源 | HTTP | 可安全讲述 | 不能直接证明 |
|---|---:|---|---|
| `https://langfuse.com/guides/user-feedback-loop` | 200 | 用户反馈可以作为反馈闭环的一部分，并需要与可追踪运行关联 | 当前项目已经收到反���、反馈已写入或所有用户都满意 |
| `https://langfuse.com/docs/observability/features/scores` | 200 | Score/反馈字段和可观测性方向；具体参数以拍摄当天页面为准 | 当前 SDK/API 参数在本地实例一定可用 |

## 断言风险与证据要求

| 说法 | 放行条件 | 当前状态 |
|---|---|---|
| 反馈可绑定 Trace/Observation | 保存脱敏反馈、Trace/Observation ID、source、value、timestamp 和当前 SDK/API 版本 | `needs-review`，页面可访问但未做受保护写入 |
| 反馈可以写成 Score 或事件 | 同一轮写入响应、关联 ID 和当前版本回读响应齐全 | `BLOCKED` |
| 反馈代表用户满意度 | 需要采样框、覆盖范围、缺失反馈和偏差分析；单条反馈不能推出总体满意度 | `BLOCKED` |
| 正负反馈可用于回归 Dataset | 反馈原文脱敏、item/run 关联、加入 Dataset 的版本和权限记录齐全 | `BLOCKED` |

## 当前运行边界

- 当前 shell 没有安全注入项目 key/secret，因此不执行反馈、Score 或事件写入。
- 历史截图、健康检查、空请求认证响应不能证明本轮反馈已回流。
- LF-08 快切视频只能讲方法和证据链，保持 `prototype / L1`；不能把示意正负反馈说成真实用户分布。
- 反馈原文必须脱敏；视频和仓库不得出现 PII、Authorization、完整 prompt 或内网地址。

## 最小证据包

1. 运行 metadata：实例版本、SDK 版本、运行时间、commit 和脱敏 run ID。
2. 脱敏反馈输入：来源、类型、取值范围、时间和缺失值策略。
3. 关联写入：Trace/Observation ID、HTTP 状态、非敏感响应正文。
4. 回读：同一 ID 的 Score/事件 JSON 与必要 UI 记录。
5. 样本审计：正例、负例、空值和抽样规则；不得只展示好评。
6. SHA-256 清单与逐条 claim review。

## 结论

LF-08 可以讲“反馈如何和 Trace 对齐、如何形成可解释 Score、如何回流 Dataset”。当前无法证明真实写入、回读或总体满意度，正式发布证据保持 `BLOCKED`。
