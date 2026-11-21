# LF-01–05 证据包模板

每集目录建议：`evidence/LF-XX/`。缺任何必填项，状态保持 `blocked`。

| 集数 | 必须保存 | 回读/验收字段 | 当前状态 |
|---|---|---|---|
| LF-01 | quickstart 命令、SDK/服务端版本、脱敏输入输出、Trace ID、UI 截图 | Trace 可刷新，输入输出一致 | 待项目 Key |
| LF-02 | session/case ID、最终回复、Trace ID、API JSON、UI 截图 | completed、trace_id、input/output、model、usage/unknown | 待项目 Key |
| LF-03 | 调用代码、Observation ID、父子树截图、API JSON | type、name、parentObservationId、status | 待项目 Key |
| LF-04 | Prompt v1/v2、label、获取命令、Trace metadata | 版本/label 与运行记录一致 | 待项目 Key |
| LF-05 | Dataset 定义、item ID、两个 run、原始输出、失败样本 | run ID、item ID、评分、版本和条件 | 待项目 Key |

## 通用字段

`checked_at`、`langfuse_version`、`sdk_version`、`runtime_version`、`git_commit`、`project_id`、`source_url`、`redaction_check`、`status`、`blocker`。

禁止保存 Secret、Bearer、PII、完整内网配置或未经脱敏的业务输入输出。
