# LF-19 证据审计（2026-11-22）

## 审计范围

本次审计检查 LAB-02 证据桥接、原始响应完整性记录、LF-16 OTEL 入口探针和当前 runtime 发现记录，目的是确认 LF-19“认证门、Trace ID 回读与证据闭环”可以怎样讲，且不越过已有证据边界。

## 检查结论

| 项目 | 结论 | 依据 |
|---|---|---|
| 原始响应文件可读 | PASS | `evidence/lab02-raw-integrity-2026-11-22.md`；JSON 文件已解析，SHA-256 清单已生成 |
| 服务健康采样 | sampled-pass | `runtime-discovery-2026-11-22-0044.md` 记录 Web health/ready 及 Gateway health；这是时间点采样 |
| Gateway readiness | BLOCKED/未配置 | raw 响应正文为 `status=unconfigured`；桥接记录注明实际 HTTP 503 |
| OTEL 入口存在 | verified | `lf16-otel-endpoint-probe-2026-11-22.md` 记录入口响应 405/204/401 |
| OTEL 认证成功 | BLOCKED | 当前环境没有项目 key/secret，401 只能证明认证门生效 |
| 新 Trace 写入 | BLOCKED | 没有受保护凭据、脱敏 payload、Trace ID 和回读响应 |
| UI/API 回读 | BLOCKED | 旧 API 路径返回 v4 `events_only` 迁移提示，未取得新 Trace |

## LF-19 可安全讲述的范围

1. 先区分三层：入口存在、认证通过、Trace 写入并可回读。
2. `OPTIONS 204` 或 `HEAD 405` 只能说明 HTTP 路由行为；空 JSON `POST 401 Invalid credentials` 只能说明请求到达认证门。
3. 只有保存了脱敏 OTLP payload、HTTP 状态和响应、返回或生成的 Trace ID、回读结果、SDK/实例版本与运行 commit，才可以把“写入成功”升级为可复核证据。
4. 当前课程与视频仍保持 `prototype / L1`；不能把本轮探针或历史调用树说成当前实例新 Trace 成功。

## 敏感信息检查

- 检查范围：桥接文档、raw 目录、完整性清单及引用的 runtime/OTEL 证据。
- 未发现项目 public key、secret key、Authorization header、个人身份信息或未脱敏请求体。
- 内网实例地址仅作为现有运行证据的上下文，课程脚本不应把它当作公开服务地址。

## 验证命令与结果

在仓库根目录执行：

```bash
python3 - <<'PY'
from pathlib import Path
import json
for p in sorted(Path('langfuse/evidence/raw').glob('*.json')):
    json.loads(p.read_text())
print('json raw parse: PASS')
PY
test -s langfuse/evidence/lab02-document-bridge-2026-11-22.md
test -s langfuse/evidence/lab02-raw-integrity-2026-11-22.md
test -s langfuse/evidence/lf19-evidence-audit-2026-11-22.md
```

结果：JSON raw parse `PASS`；三个 Markdown 文件均非空。审计不执行写入、不使用真实凭据，也不改变任何课程的证据等级。

## 未完成与下一步

要解除 `new-trace-e2e = blocked`，需在受保护环境重新运行最小 OTEL 请求，保存脱敏 payload、认证响应、Trace ID 回读和版本信息，再由主 agent 更新 LF-19 证据包与 manifest。没有这些材料时继续保持阻塞。
