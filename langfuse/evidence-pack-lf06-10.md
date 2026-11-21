# LF-06–10 证据包模板

| 集数 | 关键证据 | 真实回读字段 | 失败/阻塞 |
|---|---|---|---|
| LF-06 | Score 规则、Trace/Run ID、原始高低分样本 | score_id、value/data_type、trace/observation/run ID、evaluator 版本 | 无写入/只看平均分 |
| LF-07 | Generation JSON、模型和 usage、计时点、价格配置 | model、usageDetails、start/end、cost 或 unknown | provider 未返回 usage |
| LF-08 | 反馈原文脱敏、Trace ID、Score/事件写入、空值样本 | source、value、timestamp、trace/observation ID | 反馈无法归因 |
| LF-09 | sampling/脱敏/保留/权限配置、测试日志 | 采样规则、redaction 结果、访问审计、回滚项 | 暴露 PII 或无回滚 |
| LF-10 | Agent/检索/Tool/Generation 调用树、API JSON | type、name、parentObservationId、status、错误 | 错挂、重复或孤立节点 |

每集还保存 `input.json`（脱敏）、`output.json`、`run-command.txt`、`screenshot.png`、`environment.md`、`claim-review.md`。
