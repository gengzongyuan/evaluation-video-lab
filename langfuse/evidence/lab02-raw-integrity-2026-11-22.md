# LAB-02 原始响应完整性核验（2026-11-22）

## 范围

本次核验覆盖 `evidence/raw/` 下 LAB-02 的 8 个响应文件（7 个 JSON、1 个文本响应）。核验目标是确认文件可读、JSON 可解析、内容摘要与现有证据文档一致，并生成可复核的 SHA-256 清单。本核验不重新访问服务，也不把响应正文当成 HTTP 状态码或 Trace 写入证明。

## 核验方法

在项目根目录执行：

```bash
python3 - <<'PY'
from pathlib import Path
import hashlib, json

raw = Path("evaluation-video-lab/langfuse/evidence/raw")
for path in sorted(raw.iterdir()):
    data = path.read_bytes()
    if path.suffix == ".json":
        json.loads(data)
    print(path.name, len(data), hashlib.sha256(data).hexdigest())
PY
```

结果清单固定保存为 [`SHA256SUMS-2026-11-22.txt`](raw/SHA256SUMS-2026-11-22.txt)。以后复核可在 `raw/` 目录执行 `shasum -a 256 -c SHA256SUMS-2026-11-22.txt`。

## 结果

| 文件 | 字节数 | 结果 | 内容核对 |
|---|---:|---|---|
| `lab02-health-2026-11-22-0044.json` | 34 | PASS，JSON 可解析 | `status=OK`，`version=4.79.0` |
| `lab02-web-ready-2026-11-22-0044.json` | 34 | PASS，JSON 可解析 | `status=OK`，`version=4.79.0` |
| `lab02-gateway-health-2026-11-22-0044.json` | 15 | PASS，JSON 可解析 | `status=ok` |
| `lab02-gateway-ready-2026-11-22-0044.json` | 25 | PASS，JSON 可解析 | `status=unconfigured` |
| `lab02-minio-live-2026-11-22-0044.txt` | 0 | PASS，空正文符合 liveness 采样记录 | 空响应 |
| `lab02-health-2026-11-22.json` | 34 | PASS，JSON 可解析 | `status=OK`，`version=4.79.0` |
| `lab02-legacy-traces-endpoint-2026-11-22.json` | 487 | PASS，JSON 可解析 | v4 `events_only` 迁移提示 |
| `lab02-legacy-observations-endpoint-2026-11-22.json` | 487 | PASS，JSON 可解析 | 与 traces 路径正文一致的 v4 `events_only` 迁移提示 |

8 个文件均可读，JSON 文件均通过解析。SHA-256 清单与 `runtime-discovery-2026-11-22-0044.md`、`lab02-live-probe-2026-11-22.md` 中已登记的摘要一致；两个同正文的 legacy endpoint 文件具有相同摘要属于预期结果。

## 证据边界

- **原始文件完整性：PASS（当前工作区快照）**。本次运行没有发现截断、非法 JSON 或清单不一致。
- **响应正文的可追溯性：PASS**。清单覆盖当前 raw 目录的全部 8 个响应文件，且新增清单本身不纳入响应集合。
- **HTTP 状态码的独立证明：PARTIAL**。raw 文件只保存响应正文；HTTP 状态码、响应头和执行命令由相邻 Markdown 记录保存，未作为单独的 header/raw 文件保存。因此不得仅凭正文断言 200/503/404。
- **实时链路：BLOCKED**。这些是只读探针输出，不能证明 OTEL 写入、Worker 消费、UI/API 回读、模型调用、重启恢复或成本数据。当前 LAB-02 仍保持 `new-trace-e2e = blocked`，课程集数保持 `prototype / L1`。

## 后续复核

若要把 LAB-02 升级为可验证运行，需在受保护环境重新执行端到端 OTEL 写入，并同时保存脱敏 payload、HTTP 状态/响应、Trace ID 回读、SDK/实例版本和运行 commit；完成后重新生成本清单并更新证据桥接记录。
