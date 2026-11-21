# LF-01–03 真实录制填写表

> 这是运行记录模板，不是已通过证据。每集需要用当前实例、当前 SDK 和新运行 ID 填写；无法填写的字段保持 `BLOCKED`。

## 公共环境

```yaml
recorded_at: "YYYY-MM-DD HH:MM Asia/Shanghai"
langfuse_base_url: "[脱敏或写 internal-instance]"
langfuse_server_version: ""
sdk_name: ""
sdk_version: ""
runtime_version: ""
git_commit: ""
project_id: ""
key_source: "protected-env-file"
redaction_check: "PASS|FAIL"
```

## LF-01｜最小可观测链路

```yaml
case_id: ""
run_command_file: ""
input_file: ""
output_file: ""
trace_id: ""
observation_ids: []
ui_screenshot: ""
expected: "Trace 可刷新，输入输出与本地运行记录一致"
result: "PASS|BLOCKED|FAIL"
blocker: ""
```

必须证明：事件被记录并可查看。不能由此证明模型质量或成本准确。

## LF-02｜Trace 调用树

```yaml
case_id: ""
session_id: ""
trace_id: ""
final_status: "completed|accepted-only|error|timeout"
observation_ids: []
ui_screenshot: ""
api_response_file: ""
fields_checked: ["traceId", "type", "name", "parentObservationId", "input", "output", "model", "usage_or_unknown"]
result: "PASS|BLOCKED|FAIL"
blocker: ""
```

必须证明：同一次运行在 UI 和 API 可按 ID 找到；accepted-only 不得判 PASS。

## LF-03｜Span / Generation / Tool

```yaml
case_id: ""
trace_id: ""
span_observation_id: ""
generation_observation_id: ""
tool_observation_id: ""
parent_relationship_checked: true|false
api_response_file: ""
ui_screenshot: ""
result: "PASS|BLOCKED|FAIL"
blocker: ""
```

必须证明：类型与真实步骤一致，父子关系可回读；没有真实工具就不手工伪造 Tool 节点。

## 证据包放行

- [ ] 原始命令、输入、输出和 API JSON 已保存且脱敏
- [ ] UI 截图不含密钥、PII、内网地址和完整业务上下文
- [ ] Trace/Observation ID 与本次新运行对应
- [ ] 版本、commit、日期和 SDK 已记录
- [ ] 口播断言逐条映射到官方 URL 或运行证据
- [ ] 30 秒复述测试通过
