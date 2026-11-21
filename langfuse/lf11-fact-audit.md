# LF-11 实验比较事实审计

## 结论

LF-11 可以讲“把两个 Prompt 或模型放在同一 Dataset、同一评分规则和同一运行条件下比较”的方法，但当前仓库没有受保护项目 key、同一轮 Dataset run、Score 回读或逐 item 原始输出。因此本集只能保持 `prototype / L1`，不能说某个 Prompt 或模型已经更好。

## 可安全讲述的范围

| 主题 | 可证明范围 | 不能推出 |
|---|---|---|
| 同一 Dataset | 固定输入集合和稳定 item ID 能减少输入差异 | Dataset 代表所有真实用户、没有采样偏差 |
| 同一条件 | 固定模型、参数、评分规则、运行日期和版本有助于归因 | 只要写了同一配置就一定没有运行波动 |
| 两个 run | 保存 run ID、逐 item 输出和失败分类可以复核差异 | 没有真实 run 时可伪造差异或汇总分数 |
| 逐 item 对照 | 先看每个样本再看汇总，能发现平均值掩盖的失败 | 少数样本的差异自动具有统计显著性 |
| 成本/延迟 | 记录原始字段并对齐运行条件，才可比较 | 一次运行推出长期 P95、SLA 或总体效率 |
| 结论范围 | 结论应限定在这组数据、版本和条件 | “全面领先”“普遍更好”或业务因果结论 |

## 最小证据包

1. Dataset 名称、版本、item 数量、稳定 item ID 和脱敏输入摘要。
2. Prompt/模型/参数版本、两次 run ID、运行时间、SDK/服务端版本和运行 commit。
3. 同一评分规则、evaluator 版本、逐 item Score、失败类型和空值处理。
4. 两个 run 的原始输出摘要、成本/延迟字段；缺失值写 `unknown`，不自行估算。
5. 当前版本支持的 UI/API 回读响应，并确认每条结果与同一 item/run 关联。
6. 汇总统计、样本量、波动或置信区间的计算方法；没有统计依据时只描述观察到的差异。
7. 脱敏检查、原始文件 SHA-256 清单和逐条 claim review。

## 录制前复核

- 当前官方入口：`https://langfuse.com/docs/evaluation/experiments`、`https://langfuse.com/docs/prompt-management`。
- 录制当天重新核对 Dataset run、实验注册、Prompt 版本/label、Score 和回读字段；父页可访问不等于具体参数未变。
- 不在画面或字幕中出现项目 key、secret、Authorization、PII、完整 prompt 或内网地址。
- 若只有示意表格、历史截图、health/readiness 或空请求认证探针，字幕必须写 `prototype / L1`，不得写成当前实验结果。

## 当前状态

- 官方文档：用于能力和术语方向，具体字段待录制当天复核。
- 同 Dataset 的两个真实 run：`BLOCKED`。
- Score/失败样本回读：`BLOCKED`。
- 统计显著性或长期效果：`BLOCKED`。
- 课程状态：`prototype / L1`。

## 验证

```bash
test -s langfuse/lf11-experiment-compare-lesson.md
rg -n "同一 Dataset|同一评分规则|失败|BLOCKED|全面领先" langfuse/lf11-experiment-compare-lesson.md
```

本审计只约束课程断言和证据边界，不替代受保护环境中的 Dataset run、Score 写入、回读和统计分析。
