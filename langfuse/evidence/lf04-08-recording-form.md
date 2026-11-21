# LF-04–08 真实录制表

| 集数 | 运行/输入证据 | 回读字段 | 必须截图 | 阻塞条件 |
|---|---|---|---|---|
| LF-04 Prompt | Prompt v1/v2、label 获取命令、Trace metadata | prompt/version/label、trace_id | 管理页、调用结果 | 版本或 label 无法回指 |
| LF-05 Dataset | Dataset/item ID、两个 run、原始输出 | run_id、item_id、版本、评分 | Dataset、run、失败样本 | 样本或条件不一致 |
| LF-06 Score | 评分规则、evaluator 版本、Trace/Run ID | score_id、value、data_type、绑定对象 | Score 与原始样本 | 只有平均分或未回读 |
| LF-07 Cost | Generation JSON、模型、usage、价格配置 | model、usageDetails、latency、cost/unknown | Generation 字段 | provider 字段缺失却猜数 |
| LF-08 Feedback | 脱敏反馈、Trace ID、写入响应、空值样本 | source、value、timestamp、trace/observation ID | 反馈→Score 链路 | 无法归因或暴露 PII |

公共字段：日期、Langfuse/SDK 版本、runtime、git commit、project ID、脱敏检查、状态、阻塞原因。所有视频当前为 `prototype/L1`，填完一集也要先通过证据包门禁再升级。
