# LAB-02 Readiness Contract（2026-11-22）

## 目的与适用范围

这份契约把 LAB-02 的运行时证据拆成可独立验收的层级，供 LF-16–LF-20、LF-02/03 和后续录制使用。它只定义“什么证据可以把哪个状态往前推进”，不把健康检查、迁移提示或历史调用树当作当前 Trace 成功证据。

本契约适用于当前自托管 Langfuse v4 实例和 2026-11-22 这轮探针。任何新的运行必须重新记录时间、实例版本、SDK/OTEL 版本和运行 commit；旧 Trace、旧 API 路径或旧截图不能自动继承状态。

## 当前状态快照

| 能力层 | 当前状态 | 本轮能证明的范围 | 不能据此证明 |
|---|---|---|---|
| Web health / readiness | `sampled-pass` | 在采样时 Web health/ready 返回 200，版本为 4.79.0 | 重启恢复、Worker 消费、Trace 写入、UI/API 回读 |
| Gateway health | `sampled-pass` | 在采样时进程健康端点返回 200 | Gateway 配置完整或真实模型请求成功 |
| Gateway readiness | `blocked` | raw 正文显示 `status=unconfigured`，相邻记录标明 HTTP 503 | 未配置的具体原因、模型调用、成本和延迟 |
| v4 migration signal | `verified`（仅响应范围） | 旧 Trace/Observation 路径返回 `events_only` 迁移提示 | 所有旧 SDK 行为一致、迁移后写入成功 |
| OTEL route / auth gate | `verified`（仅探针范围） | OTEL 路径对 HEAD/OPTIONS/空 POST 的路由和认证行为可复现（405/204/401） | 有效凭据认证成功、业务 payload 被接收 |
| OTEL authentication | `blocked` | 当前无项目 key/secret；401 仅说明认证门生效 | 认证成功或项目权限正确 |
| New Trace write | `blocked` | 没有发送受保护的最小 OTLP payload | Worker 已消费、事件已落库 |
| Trace ID readback | `blocked` | 当前没有本轮新 Trace ID 和回读响应 | UI/API 与本轮写入一致 |
| Real-time latency | `blocked` | 没有 send/flush/readback 三组时间戳 | 可宣称实时可见、延迟数值或 SLA |
| LAB-02 production readiness | `blocked` | 只读探针和 raw 完整性检查通过 | 可发布的真实端到端演示 |

当前总判定固定为：`health/readiness = sampled-pass`、`migration-signal = verified`、`new-trace-e2e = blocked`。在后文所列证据齐全前，LF-02–LF-20 保持 `prototype / L1`（或脚本的 `blocked`），不得写成当前实例已成功上报 Trace。

## 状态词和升级阶梯

| 状态 | 定义 | 可对外使用的表述 |
|---|---|---|
| `sampled-pass` | 某个端点在一个带时间戳的只读采样中返回预期结果 | “采样时通过” |
| `verified` | 指定探针或响应范围已由原始响应、命令和版本记录复核 | “该探针/响应已核对” |
| `write-observed` | 本轮受保护运行发送了脱敏 payload，并保存了状态码和响应；不等同于可回读 | “观察到写入响应” |
| `e2e-verified` | 同一轮新 Trace 的写入、Trace ID、当前 v4 支持的 UI/API 回读和字段核对全部通过 | “本轮端到端已复核” |
| `ready` | `e2e-verified` 之外，画面/字幕/脱敏/版本追溯/回滚检查也通过 | “达到本集发布门” |
| `blocked` | 任一必需证据缺失、不匹配、不可安全展示或仅能靠推断补齐 | “保持阻塞，等待指定证据” |

只读端点的 `sampled-pass` 或 OTEL 路由的 `verified` 不得跳级到 `write-observed`。`write-observed` 也不得跳级到 `e2e-verified`；必须用同一 Trace ID 做回读。

## 状态迁移门

| 当前状态 | 目标状态 | 必须满足 | 失败/降级条件 |
|---|---|---|---|
| `sampled-pass` / `verified` | `write-observed` | 受保护项目 key；锁定 SDK/OTEL 版本；脱敏最小 payload；保存 HTTP 状态、响应和发送时间 | 无 key、只发空 JSON、只有截图、响应无法关联本轮运行 → `blocked` |
| `write-observed` | `e2e-verified` | 保存本轮 Trace ID；以同一 ID 在当前 v4 支持的查询方式回读；核对 trace/event 类型、名称、父子关系、时间戳和必要字段；保存原始 JSON 与脱敏 UI 截图 | Trace ID 缺失/是旧样例；只看 UI；旧 `/api/public/traces` 或 `/observations` 404 当作回读 → `blocked` |
| `e2e-verified` | `ready` | 旁白与画面一致；字幕不扩大结论；内网地址、key、secret、PII、完整 prompt 已脱敏；版本、commit、素材和证据包可回滚 | 任一敏感信息泄露、版本不可追溯、字幕超过证据范围 → `blocked` |

任何阶段发现证据属于旧运行、字段不一致、时间窗无法对齐或原始文件缺失，都应回退到 `blocked`，并保留失败材料和原因，不删除以掩盖问题。

## `e2e-verified` 最小证据包

受保护运行必须在不把秘密写入仓库的前提下生成以下材料；敏感值只保留在受保护执行环境，仓库中保存占位符、哈希或审计结论。

1. **Run metadata**：`run_id`、Asia/Shanghai 与 UTC 时间、实例版本、SDK/OTEL exporter 版本、运行 commit、脱敏目标标识。
2. **Credential provenance**：只记录凭据来源/注入方式和权限范围，不记录 key、secret 或 Authorization header。
3. **Redacted payload**：最小 OTLP payload，隐藏 input/output 中的 PII、完整 prompt、内网地址和凭据；保留足以核对 schema 的字段。
4. **Write response**：HTTP 状态、非敏感响应正文、请求开始/结束时间；Authorization 和 cookie 必须剔除。仅 `2xx` 仍只构成 `write-observed`，不能单独构成 E2E。
5. **Trace identity**：服务返回或可确定关联的本轮 Trace ID，并说明它如何从 payload/响应/回读中取得。
6. **Readback pair**：使用当前 v4 支持的 UI/API 查询方式，以同一 Trace ID 回读原始 JSON；保存脱敏截图或等价 UI 记录，并核对 trace/event 类型、名称、父子关系、状态和时间戳。
7. **Flush and timing**：SDK flush/shutdown 日志（或 OTEL exporter 等价信号）、写入时间、回读时间和计算方式。没有这三类时间戳，不得给出“实时”或具体延迟结论。
8. **Integrity and review**：证据文件 SHA-256 清单、逐字段 claim review、运行失败样本（如有）和最终 `PASS/BLOCKED` 判定。

推荐目录（文件名可按真实 runner 调整）：

```text
evidence/LAB-02/<run-id>/
  run-metadata.json
  payload.redacted.json
  write-response.json
  trace-id.txt
  readback-api.redacted.json
  readback-ui.redacted.png
  flush.log
  timing.json
  claim-review.md
  SHA256SUMS.txt
```

## 可复查命令与证据引用

只读审计可复查当前快照，不会改变状态：

```bash
cd evaluation-video-lab
python3 - <<'PY'
from pathlib import Path
import json
raw = Path('langfuse/evidence/raw')
for p in sorted(raw.glob('*.json')):
    json.loads(p.read_text())
print('JSON raw parse: PASS')
PY
(cd langfuse/evidence/raw && shasum -a 256 -c SHA256SUMS-2026-11-22.txt)
```

当前快照的主要依据：

- `evidence/lab02-document-bridge-2026-11-22.md`：三类证据的边界和总判定。
- `evidence/lab02-live-probe-2026-11-22.md`：4.79.0 health、旧 API 404 与迁移提示。
- `evidence/runtime-discovery-2026-11-22-0044.md`：分层 health/readiness 的时间点采样。
- `evidence/lf16-otel-endpoint-probe-2026-11-22.md`：OTEL 路由与认证门探针。
- `evidence/lab02-raw-integrity-2026-11-22.md`：8 个 raw 文件的 JSON 解析和 SHA-256 完整性。
- `evidence/lf19-evidence-audit-2026-11-22.md`：认证、写入、回读和实时性的逐项审计。

这些命令和文档只能复核当前只读快照；它们不会伪造、重放或补齐受保护 OTEL 运行。

## 录制和发布约束

- 可以讲：health/readiness 的层级差异、v4 `events_only` 迁移信号、OTEL 入口存在和认证门生效，以及为什么必须用 Trace ID 回读。
- 只能在 `write-observed` 后讲：本轮请求得到非空写入响应；仍须明确“尚未完成回读”。
- 只能在 `e2e-verified` 后讲：本轮 Trace 写入、当前版本回读和字段一致性已复核。
- 只能在 `ready` 后使用真实画面作为发布证据；此前画面必须标为示意、历史或探针范围。
- 当前禁止：把健康 200、OPTIONS 204、HEAD 405、空 POST 401、旧 Trace/Observation 树或历史 PNG/HTML说成新 Trace 已成功上报；把 Gateway `unconfigured` 解释成完整故障根因；给出未经时间戳和多样本支持的成本、质量、稳定性或实时延迟结论。

## 交接责任

下次受保护运行由执行者补齐 `evidence/LAB-02/<run-id>/`，并将本契约的状态快照更新为实际结果。主 agent 在确认同一 Trace ID 的写入与回读、逐字段 claim review 和敏感信息审计后，才可修改 manifest 的证据等级；没有这些材料，契约保持 `blocked`，不因视频已生成或文件已存在而自动升级。
