# LF-09 生产治理事实与来源审计

审计对象：`langfuse/lf09-production-governance-lesson.md`、`evidence-pack-lf06-10.md`、`source-verification.md`。

## 可安全讲述的范围

| 主题 | 可证明范围 | 不可推出的结论 |
|---|---|---|
| Sampling | 采样会改变可见事件范围，规则需要和关键错误监控一起设计 | 某个采样比例一定代表真实质量或长期成本 |
| 脱敏 | 可以把 input/output redaction 作为上线前检查项，并保留脱敏结果审计 | 配置了脱敏就等于所有 PII 都已被识别和删除 |
| 保留 | 保留周期、删除策略和访问审计应有明确责任与回滚/复核记录 | 官方文档页面证明当前部署已经按该策略执行 |
| 权限与密钥 | 项目权限、密钥轮换和最小权限是发布门内容 | 看到配置文件或截图就证明权限边界有效 |
| 告警 | 告警应能回到 Trace、版本和失败样本，便于定位 | 一个总量或一次健康检查证明生产稳定 |

## 需要录制当天复核的来源

- `https://langfuse.com/docs/observability/features/sampling`
- `https://langfuse.com/docs/administration/data-retention`
- 当前 Langfuse 安全、权限和密钥管理页面（以官方导航当天可访问页面为准）

页面可访问只证明文档入口存在。录制前仍要核对字段名、配置入口、Web/SDK 版本和实际权限。

## 当前项目证据状态

- 当前实例使用内网 HTTP 地址，公开视频不得暴露地址、密钥、Authorization、PII 或完整 prompt。
- 没有安全注入项目 key，因此 sampling 配置回读、redaction 实测、保留策略验证、权限审计和告警闭环均保持 `BLOCKED`。
- LF-09 只能标记为 `prototype / L1`；视频中的清单、结构图和示意画面不能写成当前部署已经安全。

## 最小证据包

1. 记录实例版本、SDK/部署版本、运行日期和 git commit。
2. 保存脱敏后的 sampling 配置、redaction 输入/输出摘要和保留策略版本。
3. 保存访问审计、密钥来源/轮换方式和最小权限范围，不保存 secret 或 Authorization。
4. 保存一条关键错误从告警到 Trace、版本和失败样本的关联证据。
5. 对原始响应和截图生成 SHA-256 清单，并完成逐条 claim review。

## 发布阻断条件

- 把示意采样比例或成本变化说成当前实例实测。
- 把“启用脱敏”说成没有 PII 风险。
- 公开视频出现内网地址、密钥、Authorization、PII 或完整 prompt。
- 没有回滚和审计记录就宣称保留/权限策略已生效。
- 只有 health/readiness 或历史截图，没有本轮治理配置和回读证据。

## 审计结论

LF-09 的课程方向和官方来源可继续制作；生产治理的真实配置、脱敏结果、保留执行、权限审计和告警闭环尚未验证，保持 `prototype / L1` 与 `BLOCKED`。
