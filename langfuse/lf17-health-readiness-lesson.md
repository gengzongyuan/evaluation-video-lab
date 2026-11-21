# LF-17｜Health 通过，为什么链路还不能用？

## 一句话结果
看完后，观众能区分进程 health、服务 readiness 和真实 Trace 写入，不再把一个 200 当成全链路通过。

## 3 分钟结构

- 0–20s：同一个部署，`/health` 返回 200，`/ready` 却返回 503。
- 20–75s：health 说明进程能响应；ready 还要检查配置、依赖和请求链路。
- 75–125s：展示本地实例采样：Web health/ready 通过，Gateway health 通过，Gateway ready `unconfigured`，MinIO liveness 通过。
- 125–160s：解释这不能替代 SDK/OTEL 新 Trace 写入、Worker 消费和 UI/API 回读。
- 160–180s：决策卡：按服务层级记录状态，缺一层就保持风险或 blocked。

## 证据边界

本集的状态来自 2026-11-22 只读探针；它证明采样时端点返回值，不证明重启恢复、备份恢复、生产安全或模型链路。公开视频应隐藏内网 IP、端口和服务拓扑细节。
