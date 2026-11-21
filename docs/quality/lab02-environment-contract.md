# LAB-02 环境契约（2026-11-22）

本契约定义 LF-02/LF-16/LF-17/LF-18 在当前自托管 Langfuse 实例上的运行时前置条件和放行口径。它只根据本轮只读探针记录环境状态，不把服务健康升级为 Trace 写入成功。

## 契约状态

- 契约版本：`ENV-LAB02-2026-11-22-C1`
- 采样时间：2026-11-22 00:44（Asia/Shanghai）
- 目标实例：`http://172.16.33.136:3000`（内网地址，仅限私有运维记录）
- Langfuse 版本：`4.79.0`
- 当前放行：`health/readiness = sampled-pass`；`migration-signal = verified`；`new-trace-e2e = blocked`
- 课程证据等级：LF-02–LF-18 继续保持 `prototype / L1`

## 运行时字段与判定

| 字段 | 采样结果 | 状态 | 允许的结论 |
|---|---|---|---|
| Web `/api/public/health?failIfDatabaseUnavailable=true` | HTTP 200，`status=OK`，`version=4.79.0` | PASS（时间点） | Web/数据库健康检查在采样时通过 |
| Web `/api/public/ready` | HTTP 200，`status=OK`，`version=4.79.0` | PASS（时间点） | Web readiness 在采样时通过 |
| Gateway `/health` | HTTP 200，`status=ok` | PASS（时间点） | Gateway 进程 health 在采样时通过 |
| Gateway `/ready` | HTTP 503，`status=unconfigured` | RISK | Gateway 请求链路未配置，不能按可用处理 |
| MinIO `/minio/health/live` | HTTP 200，空正文 | PASS（时间点） | 对象存储 liveness 在采样时通过 |
| 旧 `/api/public/traces`、`/observations` | HTTP 404，v4 `events_only` 迁移提示 | VERIFIED MIGRATION SIGNAL | 旧回读路径不可用，应采用当前 SDK/OTEL 方向 |
| OTEL 入口 | 空 POST HTTP 401；OPTIONS HTTP 204 | AUTH GATE | 入口可达且要求认证；不代表 payload 已写入 |
| `LANGFUSE_PUBLIC_KEY`、`LANGFUSE_SECRET_KEY`、`LANGFUSE_BASE_URL/HOST` | 当前 shell 均缺失 | BLOCKED | 不执行写入，不猜测或打印凭据 |

## 放行规则

只有以下条件全部满足，才可把 `new-trace-e2e` 从 `blocked` 改为 `verified`：

1. 在受保护环境注入项目 Public/Secret Key 和 Base URL；日志、证据和截图不得包含 Secret。
2. 锁定并记录 SDK 版本、Langfuse 实例版本、运行 commit 和采样时间。
3. 使用当前 v4 events-only 支持的 SDK/OTEL 发送最小脱敏 payload；保存请求状态码、响应和脱敏 payload 摘要。
4. 保存新 Trace ID，并以当前版本支持的查询/UI 路径回读；同时记录 UI/API 一致性结果。
5. 对原始响应生成 SHA-256 清单，确保命令、版本和证据文件可复查。
6. Gateway readiness 若仍为 `503 unconfigured`，必须作为未解决风险记录，不得把端到端链路写成生产就绪。

## 明确禁止的升级

- 不得用 health/ready、Gateway health、MinIO liveness 证明 OTEL ingestion、Worker 消费、UI/API 回读、模型调用、成本或稳定性。
- 不得把历史 Trace/Observation 树当作当前 4.79.0 新运行结果。
- 不得把旧 endpoint 的 404 迁移提示或 OTEL 空请求的 401 当作写入成功。
- 不得在缺少项目 Key 时伪造 Trace ID、发送业务数据或将课程状态升为 verified。

## 证据索引

- 运行时采样：[`langfuse/evidence/runtime-discovery-2026-11-22-0044.md`](../../langfuse/evidence/runtime-discovery-2026-11-22-0044.md)
- 旧 API 探针：[`langfuse/evidence/lab02-live-probe-2026-11-22.md`](../../langfuse/evidence/lab02-live-probe-2026-11-22.md)
- 证据桥接：[`langfuse/evidence/lab02-document-bridge-2026-11-22.md`](../../langfuse/evidence/lab02-document-bridge-2026-11-22.md)
- 原始完整性：[`langfuse/evidence/lab02-raw-integrity-2026-11-22.md`](../../langfuse/evidence/lab02-raw-integrity-2026-11-22.md)
- 原始响应清单：[`langfuse/evidence/raw/SHA256SUMS-2026-11-22.txt`](../../langfuse/evidence/raw/SHA256SUMS-2026-11-22.txt)

## 复核命令

```bash
cd evaluation-video-lab
python3 - <<'PY'
from pathlib import Path
import json
raw = Path('langfuse/evidence/raw')
for name in ('lab02-health-2026-11-22-0044.json',
             'lab02-web-ready-2026-11-22-0044.json',
             'lab02-gateway-health-2026-11-22-0044.json',
             'lab02-gateway-ready-2026-11-22-0044.json'):
    print(name, json.loads((raw / name).read_text()))
PY
(cd langfuse/evidence/raw && shasum -a 256 -c SHA256SUMS-2026-11-22.txt)
```

本契约是时间点环境记录，不是重启恢复、备份恢复、生产安全或端到端发布验收。
