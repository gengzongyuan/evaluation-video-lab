# LF-18｜Gateway health 正常，为什么 readiness 还是 unconfigured？

## 一句话结果
看完后，观众能把 Gateway 的进程存活、配置就绪和真实模型请求分成三层检查。

## 3 分钟结构

- 0–20s：`/health` 返回 200，但 `/ready` 返回 503 `unconfigured`。
- 20–70s：health 只检查进程响应；ready 还要检查 service key、provider 或路由配置。
- 70–125s：展示安全化探针结果：只保留状态，不展示内网 IP、密钥或 provider 配置。
- 125–160s：说明当前 Langfuse Trace 写入不依赖 Gateway，但模型请求链路若依赖 Gateway 必须单独修复并重测。
- 160–180s：决策卡：Gateway 未 ready 时，不能把模型请求、成本或延迟视频说成生产证据。

## 证据边界

当前结论只来自时间点端点探针；没有修改 Gateway 配置，也没有发送模型请求。`unconfigured` 是风险信号，不是失败原因的完整诊断。发布前必须在受保护环境核对配置、凭据、路由和回滚。
