# LF-02 Trace 证据记录

## 当前结论

当前实例健康端点已验证：`http://172.16.33.136:3000/api/public/health?failIfDatabaseUnavailable=true` 返回 `status=OK, version=4.79.0`（2026-11-21）。

证据桥接索引见 `evidence/lab02-document-bridge-2026-11-22.md`；现场探针记录见 `evidence/lab02-live-probe-2026-11-22.md`，分层运行时采样见 `evidence/runtime-discovery-2026-11-22-0044.md`；健康端点返回 `OK / 4.79.0`，而旧 `/api/public/traces` 与 `/api/public/observations` 均返回 HTTP 404，并明确提示该实例运行在 v4 `events_only` 模式，应迁移到 OTEL 写入协议。因此，本轮不能把历史 HTML/PNG 回读当成当前版本的实时证据。

本仓库没有可安全使用的项目 Secret，也没有在当前工作区安装 Langfuse SDK，因此本轮**没有声称新建 Trace**。已有历史实验文档记录过一次 API 回读：HTTP 200、示例 Trace ID `20c59f22901395c45fca45debec026e2`，包含根 `AGENT` Observation 和一个 `GENERATION` Observation，最终输出为 `LAB01_READY`。该记录来自外部实验文档，不能替代当前版本重跑。

## 视频可讲的知识点

- Trace 是一次工作单元；Observation 描述其中的步骤。
- 模型调用使用 `generation` 语义，工具或普通步骤使用更具体的 Observation 类型。
- UI 看到 Trace 只是定位入口；可靠验收还要用 Trace ID/API 回读，并核对 input/output、model、usage（或明确 unknown）和版本 metadata。
- `accepted` 不等于完成；必须等最终回复和 completed 状态。

## 证据来源

- 官方：<https://langfuse.com/docs/observability/overview>
- 官方：<https://langfuse.com/docs/observability/data-model>
- 本地实例健康和部署记录：`LANGFUSE_DEPLOYED_INSTANCE_172.16.33.136.md`
- 历史实验协议与 API 回读边界：`/Users/bigtree/Documents/ChatGPT/评测保障体系/docs/08-harness-langfuse/03-experiments/v0.5/lab-01-execution-protocol.html`

## 当前放行状态

- 课程脚本：可讲（L1，方法与历史证据边界已写清）。
- 正式产品演示：BLOCKED，待重新注入项目 Key、运行 SDK/Harness、取得新 Trace ID，并保存脱敏 UI/API 证据。
- 禁止口播： “今天已经在当前实例成功写入了一条新 Trace” 或 “这条 Trace 代表模型稳定性”。
