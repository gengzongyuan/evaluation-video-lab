# LF-09–12 真实录制表

| 集数 | 证据包 | 回读/对照 | 放行条件 | 阻塞条件 |
|---|---|---|---|---|
| LF-09 治理 | sampling、脱敏、保留、权限配置与测试日志 | 规则、redaction、审计、回滚 | 无秘密/PII，恢复路径存在 | 只看页面或无回滚 |
| LF-10 Agent | Agent/检索/Tool/Generation 树、API JSON | type/name/parentObservationId/status | 真实调度无错挂/重复 | 只有历史树 |
| LF-11 双 run | 同 Dataset、v1/v2 run、逐 item 输出、失败分类 | run ID、条件、汇总和失败样本 | 同条件可复现 | 样本或评分不一致 |
| LF-12 排障 | 异常 Trace、根因、修复 commit、回归 run、告警 | 修复前后、版本、回归结果 | 失败样本保留，回归通过 | 只有 Dashboard 截图 |

公共证据：`run-command.txt`、脱敏 `input/output`、原始 API JSON、UI 截图、环境版本、claim review。缺项目 Key、旧 Trace 或字段未核对时状态为 `blocked`。
