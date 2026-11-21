# LAB-02 runtime discovery（2026-11-22 00:44 Asia/Shanghai）

## 目的

对当前自托管 Langfuse 节点做一次只读端点核验，确认 Web、Gateway 和对象存储的采样状态。该记录不包含项目 key，不提交 Trace、Score 或 Dataset，也不把健康端点当成写入成功证明。

## 采样结果

| 端点 | HTTP | 响应摘要 | 结论 |
|---|---:|---|---|
| `http://172.16.33.136:3000/api/public/health?failIfDatabaseUnavailable=true` | 200 | `{"status":"OK","version":"4.79.0"}` | Web 健康检查在采样时通过 |
| `http://172.16.33.136:3000/api/public/ready` | 200 | `{"status":"OK","version":"4.79.0"}` | Web readiness 在采样时通过 |
| `http://172.16.33.136:3031/health` | 200 | `{"status":"ok"}` | Gateway 进程 health 在采样时通过 |
| `http://172.16.33.136:3031/ready` | 503 | `{"status":"unconfigured"}` | Gateway 请求链路未配置，保持风险记录 |
| `http://172.16.33.136:9090/minio/health/live` | 200 | 空正文 | MinIO liveness 在采样时通过 |

采样命令均使用 `curl -sS --max-time 8`。原始正文保存在同目录 `raw/`：

- `lab02-health-2026-11-22-0044.json`
- `lab02-web-ready-2026-11-22-0044.json`
- `lab02-gateway-health-2026-11-22-0044.json`
- `lab02-gateway-ready-2026-11-22-0044.json`
- `lab02-minio-live-2026-11-22-0044.txt`

## SHA-256

```text
a29ee2b15c494311c52521766e44af56a3ad2248e7a8ab465e5206463c13d288  raw/lab02-gateway-health-2026-11-22-0044.json
c0a087627f000e9527d77ea21057ba9d41b8bf1e589903a8266b56a81084d612  raw/lab02-gateway-ready-2026-11-22-0044.json
66a841e8d421716d4b2ad27b61f177d50cfd624c7a37d7d8c5333656f056b6be  raw/lab02-health-2026-11-22-0044.json
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  raw/lab02-minio-live-2026-11-22-0044.txt
66a841e8d421716d4b2ad27b61f177d50cfd624c7a37d7d8c5333656f056b6be  raw/lab02-web-ready-2026-11-22-0044.json
```

## 判定边界

- **PASS（采样端点）**：Web health/ready、Gateway health、MinIO liveness 在本次采样返回预期状态。
- **RISK（Gateway）**：Gateway `/ready` 返回 `503 unconfigured`，不能把网关请求路径说成已配置或可用。
- **BLOCKED（LF-02 新 Trace）**：当前 shell 仍无项目 Key/Base URL，未执行 OTEL 写入；本记录不能证明 Trace ingestion、Worker 消费、UI/API 回读、模型调用或成本数据。
- 这是时间点检查，不是重启恢复、备份恢复或生产安全验收。
