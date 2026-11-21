# LF-19：OTEL 认证门、Trace ID 回读与证据闭环

- **时长**：约 180 秒
- **级别**：迁移 / 生产
- **状态**：`prototype / L1`
- **一句话结果**：看到 OTEL 入口返回 401，只能证明入口存在并要求认证；只有拿到脱敏写入响应、Trace ID 和回读结果，才能说“链路跑通”。
- **本集边界**：当前环境没有项目 `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY`，本集不执行真实写入，不伪造 Trace ID，不把 401 当作成功。

## 180 秒时间轴

### 0–20 秒：开场钩子

**口播**：

> 你把请求发到 Langfuse 的 OTEL 地址，返回 401。这个结果到底说明什么？它说明认证门生效，不说明 Trace 已经写进去。今天用三层证据，把“入口能访问”和“数据真的落下去”分开。

**画面**：标题卡；依次出现“入口存在”“认证通过”“写入可回读”三张卡片，第三张先标为待验证。

### 20–55 秒：先确认迁移方向

**口播**：

> Langfuse v4 的旧 Trace 和 Observation 路径会返回 `events_only` 的迁移提示。官方迁移方向是使用 OpenTelemetry，入口是 `/api/public/otel/v1/traces`。这一步回答的是“我应该打哪个入口”，不是“我的请求已经成功”。

**画面**：左侧旧 API 404/迁移提示，右侧 OTEL 路径；用箭头标出“路径迁移”，不要把 404 画成服务宕机。

**证据卡**：

- `evidence/lab02-live-probe-2026-11-22.md`
- `evidence/lf16-otel-endpoint-probe-2026-11-22.md`

### 55–95 秒：解释 401 认证门

**口播**：

> 对 OTEL 入口发送空 JSON 探针，当前实例返回 `401 Invalid credentials`。这能证明三件事：域名和路径可达、服务识别到请求、认证凭据缺失或不合法。它不能证明 payload 被接收，也不能证明 Worker 已消费，更不能证明 UI 里能查到 Trace。

**画面**：探针结果四行：`OPTIONS 204`、`HEAD 405`、`POST 401`、`写入成功？未知`。把 401 旁边标成“认证门”，不是“失败写入”。

### 95–135 秒：讲清 Trace ID 回读闭环

**口播**：

> 真正的最小闭环需要四份证据。第一，固定 SDK 或 OTEL 版本；第二，使用受保护的项目 key 发送脱敏 payload；第三，保存 HTTP 状态、响应和返回的 Trace ID；第四，用相同实例和时间窗回读，并核对服务端的 Trace、Observation 或等价事件。少了第四步，就只能说“请求发出去了”。

**画面**：四步环形图：版本 → 脱敏写入 → Trace ID → 回读核对。每一步点亮后才进入下一步。

### 135–165 秒：给出安全演示模板

**口播**：

> 录制时可以展示伪代码，但要把占位符留在画面里：`LANGFUSE_PUBLIC_KEY`、`LANGFUSE_SECRET_KEY`、`TRACE_ID`。不要录入真实密钥，不要把用户输入、模型原文或内网地址放进公开视频。演示结果分三级：入口探针是 `sampled-pass`，认证后的写入响应是 `write-observed`，带 Trace ID 的回读才是 `e2e-verified`。

**画面**：终端伪代码与证据等级标签；真实 key 区域用黑框占位。

### 165–180 秒：收束与 CTA

**口播**：

> 下一集我们会把 headers、时间戳和 flush 讲清楚，继续追踪为什么“发出请求”不等于“马上可见”。如果你复现实验，请同时保存请求版本、脱敏 payload、状态码、Trace ID 和回读截图；缺一项，就把结论降级。

**画面**：检查清单和 CTA：“收藏这四份证据，复现后再升级结论”。

## 演示步骤（录制版）

1. 展示当前官方迁移说明或仓库的迁移证据，标出旧 API 的 `events_only` 提示。
2. 展示 OTEL endpoint 的 `OPTIONS 204` 与空 JSON `POST 401`，保留采样时间和响应正文。
3. 在代码编辑器中展示伪代码和占位环境变量；不读取或打印任何真实 key。
4. 展示证据模板字段：`sdk_version`、`endpoint`、`payload_hash`、`http_status`、`trace_id`、`readback_status`、`captured_at`。
5. 最后显示三个状态：`sampled-pass`、`write-observed`、`e2e-verified`，说明本环境当前停在第一层认证探针，真实 E2E 为 `BLOCKED`。

## 事实与证据边界

| 结论 | 当前等级 | 依据 | 不能推出 |
|---|---|---|---|
| OTEL 路径存在且认证门生效 | `verified`（探针范围） | `evidence/lf16-otel-endpoint-probe-2026-11-22.md` | 不能推出 Trace 写入成功 |
| 旧 API 返回 v4 `events_only` 迁移提示 | `verified`（响应范围） | `evidence/lab02-live-probe-2026-11-22.md` | 不能推出所有旧 SDK 行为一致 |
| 当前实例完成新 Trace E2E | `BLOCKED` | 缺少受保护项目 key 和回读证据 | 不得在标题、口播或字幕写成已跑通 |

## 发布前检查

- [ ] 视频约 180 秒，包含音频和视频流。
- [ ] 字幕逐字复核 401、`events_only`、OTEL endpoint 和 `BLOCKED` 标签。
- [ ] 不含真实 key、secret、PII、未脱敏 prompt 或内网截图。
- [ ] 证据文件能回到采样时间、原始响应和命令。
- [ ] 若补齐真实凭据，必须重新录制写入、Trace ID 和回读三段，并把 claim level 从 `L1` 逐级升级，不能直接改成 verified。

## 参考来源

- `langfuse/evidence/lab02-live-probe-2026-11-22.md`
- `langfuse/evidence/lf16-otel-endpoint-probe-2026-11-22.md`
- `langfuse/evidence/lab02-document-bridge-2026-11-22.md`
- `langfuse/evidence/lab02-raw-integrity-2026-11-22.md`
- Langfuse 官方当前文档入口（以仓库 `source-link-audit-2026-11-22.md` 记录的可访问页面为准）
