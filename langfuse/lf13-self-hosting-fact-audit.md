# LF-13 事实审计：自托管架构与健康检查

任务：LF13-S1。官方文档核对日期：2026-11-23（Asia/Shanghai）；本集为概念课程，当前无项目 key，未执行真实运行。

## 结论

这集要守住一句话：**Web/Worker/数据库/队列/对象存储各负其责；health/readiness 是时间点信号，不等于全链路写入、消费、回读或生产安全。**

- 应用分成 Langfuse Web 和 Langfuse Worker 两个容器。
- health 200 不证明 SDK 写入、Worker 消费、数据库持久化或对象存储正常。
- 备份需恢复演练；配置备份不等于能恢复。状态保持 `prototype / L1`。

## 官方组件职责（2026-11-23 读取）

来源：<https://langfuse.com/self-hosting/deployment/infrastructure/containers>

| 组件 | 职责 |
|---|---|
| Langfuse Web | 服务 Console 和 API |
| Langfuse Worker | 后台任务，如发邮件、处理事件 |
| PostgreSQL | 事务数据 |
| ClickHouse | 观测数据 |
| Redis/Valkey | 缓存与任务队列 |
| S3/blob | 原始事件与多媒体附件 |

高可用至少两个 Web 实例。

## 与现有 LF-13 审计的对齐

`lf13-fact-audit.md` 已覆盖组件职责、health/readiness、版本部署、备份恢复、最小证据包。本文件补上官方容器划分和存储职责。

## 与其他 agent 的冲突

- 若有人把 health 200 当成全链路验收，与本审计冲突。
- 若有人把配置备份当成能恢复，或 latest 当版本号，与本审计冲突。

## 需要冻结的字段

- 状态：`prototype / L1`；全链路写入/消费/回读、备份恢复、生产安全 `BLOCKED`。
- 组件：Web、Worker、PostgreSQL、ClickHouse、Redis、S3/blob。
- 禁出现：内网地址、真实 key / secret、Authorization 值、登录信息、PII。

## 依据

- 容器：<https://langfuse.com/self-hosting/deployment/infrastructure/containers>
- 健康端点：<https://langfuse.com/self-hosting/configuration/health-readiness-endpoints>

仓库内证据：`langfuse/lf13-fact-audit.md`、`langfuse/lf13-self-hosting-lesson.md`、`langfuse/lf17-health-readiness-fact-audit.md`。

## 产物与验证

独占产物：本文件。未改视频、字幕、播放器、manifest 或 `docs/quality/00-project-state.md`，未 git commit。

## 风险与下一步

没有项目 key，全链路写入/消费/回读、备份恢复未验证。由主 agent 保持组件职责与 health 边界口径。
