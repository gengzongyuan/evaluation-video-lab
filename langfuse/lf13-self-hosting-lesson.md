# LF-13｜Langfuse 自托管架构与健康检查

## 一句话结果
看完后，观众能说清 Web、Worker、数据库、队列和对象存储各自承担什么，并用健康端点判断“服务活着”还是“链路已验收”。

## 3 分钟结构

- 0–25s：浏览器能打开，不代表 Trace 写入、Worker 消费和对象存储都正常。
- 25–85s：展示 Web/UI、Worker、PostgreSQL/ClickHouse、Redis、MinIO/S3 的职责关系。
- 85–130s：运行 `/api/public/health`、`/api/public/ready` 和 Worker health，记录版本与返回状态。
- 130–165s：解释版本固定、镜像 digest、备份和恢复检查。
- 165–180s：决策卡：先核对服务链路，再录制产品知识。

## 实例证据

当前实例记录为 Langfuse 4.79.0；health 返回 `status=OK`。这只能证明该端点在核验时正常，不能证明 SDK 写入、Worker 消费、对象存储或公网安全全部通过。公开视频不得暴露内网地址、密钥和登录信息。

来源：<https://langfuse.com/self-hosting>、<https://langfuse.com/docs/deployment>。
