# LF-09 事实审计：Sampling、脱敏、保留和生产治理

任务：LF09-S1。官方文档核对日期：2026-11-23（Asia/Shanghai）；本集为概念课程，当前无项目 key，未执行真实运行。

## 结论

这集要守住一句话：**sampling、脱敏、保留、权限、告警是上线前治理门；配置了不等于已安全，启用脱敏不等于没有 PII 风险。**

- sampling 控制采集量，客户端生效；脱敏在数据离开应用前进行；保留控制数据保存时长。
- 治理配置需回读和审计；health/历史截图不能证明生产安全。状态保持 `prototype / L1`。

## 官方治理机制（2026-11-23 读取）

来源：Sampling、Masking、Data Retention 官方页。

| 主题 | 官方口径 | 边界 |
|---|---|---|
| Sampling | 客户端控制采集量；`LANGFUSE_SAMPLE_RATE` 或 `sample_rate`/`sampleRate`，取值 0–1 | 某采样比例不代表真实质量或长期成本 |
| Masking | 用 masking 函数在 trace 数据离开应用前脱敏 input/output/metadata | 启用脱敏不等于所有 PII 已识别删除 |
| Data Retention | 控制 Traces、Observations、Scores、Media Assets 的保存时长；同策略适用于 Halo 会话 | 页面存在不等于当前部署已按策略执行 |
| 权限/密钥 | 最小权限、密钥轮换是发布门 | 截图不证明权限边界有效 |
| 告警 | 应能回到 Trace、版本和失败样本 | 一次健康检查不证明生产稳定 |

## 与现有 LF-09 审计的对齐

`lf09-fact-audit.md` 已覆盖可讲范围、来源、最小证据包、阻断条件。本文件补上官方具体字段：`LANGFUSE_SAMPLE_RATE`（0–1）、masking 在数据离开前、retention 覆盖的对象类型。

## 与其他 agent 的冲突

- 若有人把启用脱敏说成没有 PII 风险，与本审计冲突。
- 若有人把示意采样比例/成本变化说成当前实例实测，与本审计冲突。
- 若有人只有 health/readiness 就宣称治理策略已生效，与本审计冲突。

## 需要冻结的字段

- 状态：`prototype / L1`；sampling 回读、redaction 实测、保留验证、权限审计、告警闭环 `BLOCKED`。
- sampling：LANGFUSE_SAMPLE_RATE，0–1，客户端。
- masking：数据离开应用前脱敏。
- 禁出现：内网地址、真实 key / secret、Authorization 值、登录信息、PII、完整 prompt。

## 依据

官方页面，2026-11-23 以 Markdown 端点读取：

- Sampling：<https://langfuse.com/docs/observability/features/sampling>
- Masking：<https://langfuse.com/docs/observability/features/masking>
- Data Retention：<https://langfuse.com/docs/administration/data-retention>

仓库内证据：

- `langfuse/lf09-fact-audit.md`
- `langfuse/lf09-production-governance-lesson.md`

## 产物与验证

独占产物：本文件。未改视频、字幕、播放器、manifest 或 `docs/quality/00-project-state.md`，未 git commit。

## 风险、缺口与未完成

- 没有项目 key，治理配置回读、脱敏实测、保留验证、权限审计、告警闭环全部未验证。
- 公开视频不得暴露内网地址、密钥、PII。

## 建议下一步

由主 agent 把 LF-09 口播补上官方具体字段。等级升级只能等受保护治理配置与回读证据。
