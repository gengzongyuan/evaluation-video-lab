# LAB-02 当前实例现场探针（2026-11-22）

## 目的

确认当前自托管 Langfuse 实例的版本、健康状态，以及历史证据使用的旧版 Trace/Observation API 是否仍可回读。该探针只访问公开健康端点和不带凭据的 API 路径，不提交业务数据，也不包含项目 key。

## 环境

- 目标：`http://172.16.33.136:3000`
- 执行时间：2026-11-22 00:38:14 Asia/Shanghai（响应 HTTP Date 为 2026-11-21 16:38 UTC）
- 版本：4.79.0（由健康端点返回）
- 历史 Trace ID：`454adc908912013e94732eb059ae8e89`（仅用于验证旧回读路径，不代表本次新运行）

## 可复现命令

```bash
curl -sS --max-time 8 \
  'http://172.16.33.136:3000/api/public/health?failIfDatabaseUnavailable=true'

curl -sS --max-time 8 \
  'http://172.16.33.136:3000/api/public/traces/454adc908912013e94732eb059ae8e89'

curl -sS --max-time 8 \
  'http://172.16.33.136:3000/api/public/observations?traceId=454adc908912013e94732eb059ae8e89'
```

## 原始响应摘要

健康检查返回 HTTP 200：

```json
{"status":"OK","version":"4.79.0"}
```

两个旧版回读路径均返回 HTTP 404，响应正文一致：

```json
{
  "message": "This endpoint is not available on deployments running in Langfuse v4 events_only mode. Upgrade to the latest Langfuse SDKs, which send traces via OpenTelemetry, or send traces directly to POST /api/public/otel/v1/traces. Scores can still be sent via POST /api/public/scores. Docs: https://langfuse.com/docs/observability/sdk/upgrade-path https://langfuse.com/integrations/native/opentelemetry/migration-to-v4.md Learn more about Langfuse v4 at https://langfuse.com/docs/v4."
}
```

完整正文保存在：

- `raw/lab02-health-2026-11-22.json`
- `raw/lab02-legacy-traces-endpoint-2026-11-22.json`
- `raw/lab02-legacy-observations-endpoint-2026-11-22.json`

SHA-256：

```text
66a841e8d421716d4b2ad27b61f177d50cfd624c7a37d7d8c5333656f056b6be  raw/lab02-health-2026-11-22.json
34f752c5e3a1217e9ffadbc1d8998b55ae9c7642bfbb8cce8e394b9a0be12de3  raw/lab02-legacy-observations-endpoint-2026-11-22.json
34f752c5e3a1217e9ffadbc1d8998b55ae9c7642bfbb8cce8e394b9a0be12de3  raw/lab02-legacy-traces-endpoint-2026-11-22.json
```

## 结论与边界

- **PASS（实例健康）**：实例可访问，数据库健康检查返回 `OK`，版本为 4.79.0。
- **BLOCKED（LF-02 新证据）**：没有项目 key 注入，也没有按当前 v4 OTEL 协议新写入 Trace；因此不能把历史 HTML/PNG 中的 Observation 树当作本次版本的实时回读。
- **已确认迁移方向**：当前部署的旧 `/api/public/traces` 与 `/api/public/observations` 不可用；下一次受保护运行应使用升级后的 SDK/OTEL `POST /api/public/otel/v1/traces`，再用当前版本支持的查询方式核对 Trace/Observation。
- **禁止断言**：本探针不能证明 Trace 写入成功、UI 与 API 一致、模型质量、成本或稳定性。

