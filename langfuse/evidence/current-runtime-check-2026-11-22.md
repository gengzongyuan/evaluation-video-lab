# 当前运行环境检查（2026-11-22）

## 只读结果

```text
LANGFUSE_PUBLIC_KEY=missing
LANGFUSE_SECRET_KEY=missing
LANGFUSE_BASE_URL=missing
LANGFUSE_HOST=missing
health={"status":"OK","version":"4.79.0"}
episodes=15
manifest validation passed
video_qa_bad=[]
```

## 判定

- health 端点正常，说明 Web/数据库健康检查在本次请求时返回 OK。
- 没有发现当前 shell 中的项目 Key 或 Base URL，因此本轮没有尝试写入 Trace、Dataset 或 Score，也没有打印或猜测凭据。
- 15 集 manifest 和视频基础 QA 仍通过，但不改变真实实例证据状态。

## 下一步最小动作

在受保护环境中注入项目 Key 后，先跑 LF-01 的脱敏 quickstart，保存新 Trace ID、UI/API 回读和版本；成功后再复制证据包格式到 LF-02/03。没有 Key 时保持 `blocked`，不把 health 或历史 Trace 升级为新运行证据。
