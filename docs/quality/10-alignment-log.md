# 多 Agent 对齐与冲突台账

本文件记录不同 agent 对同一目标、字段、状态、责任或验证结论的理解差异。只有主 agent 可以关闭冲突、升级契约版本和标记契约冻结。

## 当前对齐摘要

- 当前对齐轮次：0
- 当前契约版本：C-000
- 共享契约状态：open
- 未决冲突数：0
- 当前成熟度：not_assessed

## 对齐规则

- `open`：存在不同理解，依赖该结论的任务不得启动。
- `resolving`：已指定验证动作，仍不得把下游当作已对齐。
- `aligned_pending_validation`：文字口径暂时统一，但验证尚未区分不同解释。
- `resolved`：证据支持结论，主 agent 已更新契约和版本。
- `contract_frozen`：样板、validator、precheck 或真实 smoke run 通过，下游可执行。
- `accepted`：最终责任人接受剩余限制和风险。

## 冲突记录

| conflict_id | topic | agent_a_view | agent_b_view | hidden_assumptions | evidence_needed | owner | decision_owner | resolution | contract_change | verification | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C-001 |  |  |  |  |  |  |  |  |  |  | open |

## 契约变更记录

| contract_version | alignment_round | 变更内容 | 受影响任务 | 冻结证据 | 主 agent 结论 | 日期 |
| --- | --- | --- | --- | --- | --- | --- |
| C-000 | 0 | 初始化，尚未冻结 |  |  |  |  |

## 交接核对项

- [ ] 我的理解已写明
- [ ] 隐含假设已写明
- [ ] 能证明与不能证明的范围已分开
- [ ] 冲突已关联到 `conflict_id`
- [ ] 需要冻结的字段和状态已列出
- [ ] 验证命令、结果和证据路径可复查
