# LF-19/LF-20 来源与发布审计（2026-11-22）

## 结论

LF-19 和 LF-20 可以作为 `prototype / L1` 课程包继续制作。两集的脚本明确区分了官方文档说明、只读探针和真实运行证据；当前没有项目 key，因此不能把 OTEL 写入、Trace 回读、flush 行为或实时延迟写成已验证事实。发布前必须重新核对官方页面、实例版本和脱敏运行证据。

## 官方来源与录制前复核

| 课程 | 主题 | 当前官方入口 | 录制当天必须核对 | 当前状态 |
|---|---|---|---|---|
| LF-19 | v4 迁移、OTEL endpoint、认证门、Trace 回读 | `https://langfuse.com/docs`、当前 Langfuse OTEL/SDK 指南 | v4 events-only 迁移说明、OTLP HTTP endpoint、认证 header、当前回读方式和响应字段 | `needs-review` |
| LF-20 | headers、时间戳、资源属性、flush、重试、实时性 | `https://langfuse.com/docs/observability`、当前 SDK/OTEL 指南 | endpoint 与 Content-Type、认证方式、timestamp/resource 属性格式、exporter flush/shutdown 和重试语义 | `needs-review` |

仓库的 [`source-link-audit-2026-11-22.md`](source-link-audit-2026-11-22.md) 记录了旧深链接返回 404 后采用的父页或当前指南入口。入口页面可访问只证明文档存在，不证明脚本中的具体字段、参数或当前实例行为。

## 事实分层

| 说法 | 可用证据 | 发布前结论 |
|---|---|---|
| 旧 API 返回 v4 `events_only` 迁移提示 | `evidence/lab02-live-probe-2026-11-22.md` | 可以讲探针观察，不能推导所有旧 SDK 行为一致 |
| OTEL 路由存在并要求认证 | `evidence/lf16-otel-endpoint-probe-2026-11-22.md` 的 405/204/401 | 可以讲认证门，不能说写入成功 |
| headers/payload 被接收 | 需要受保护 key、锁定版本、脱敏 payload、HTTP 响应 | 当前 `BLOCKED` |
| flush 后事件可回读 | 需要 flush/shutdown 日志、同一 Trace ID 和当前 v4 查询回读 | 当前 `BLOCKED` |
| 实时延迟达到目标 | 需要多次 `sent_at`、`response_at`、`readback_at` 和统计口径 | 当前 `BLOCKED` |

## 发布门禁

1. 页面标题、URL、核对日期和 Langfuse/SDK 版本写入证据卡。
2. 任何真实运行都使用受保护环境变量；视频、字幕、仓库不出现 key、secret、Authorization、PII、完整 prompt 或内网地址。
3. LF-19 至少保存脱敏 payload、HTTP 状态/响应、Trace ID 和同一 ID 的回读响应；缺少回读时最多标为 `write-observed`。
4. LF-20 额外保存 headers 来源、timestamp/resource 字段、flush/shutdown、重试次数和多次可见性时间戳；没有这些材料不得给出“实时”或具体延迟结论。
5. 视频与字幕必须保留 `prototype / L1` 和 `BLOCKED` 标签，直到证据包满足 `e2e-verified`；不能因 MP4 可播放而升级状态。

## 验证命令

```bash
cd evaluation-video-lab
test -s langfuse/lf19-otel-auth-readback-lesson.md
test -s langfuse/lf20-otel-headers-realtime-lesson.md
python3 langfuse/validate_manifest.py
rg -n "BLOCKED|prototype / L1|source-link-audit" langfuse/lf19-otel-auth-readback-lesson.md langfuse/lf20-otel-headers-realtime-lesson.md
```

这些命令只能验证课程资产和边界文字，不能替代受保护 OTEL 写入与回读。当前审计结论保持：`health/readiness = sampled-pass`、`OTEL route/auth gate = verified`、`new-trace-e2e = blocked`。
