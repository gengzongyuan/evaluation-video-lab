# Langfuse LF-01–LF-18 系列缺口审计（2026-11-22）

## 审计口径

审计对象是 `langfuse/manifest.json` 登记的 18 集。脚本与视频路径按 manifest 的项目根相对路径解析；字幕按 `langfuse/captions/LF-XX.srt` 和 `.vtt` 检查。证据等级以 manifest 的 `claim_level` 为准，不根据文件存在性推高等级。

## 机器核验结果

| 项目 | 结果 |
|---|---:|
| 登记集数 | 18 |
| 脚本存在 | 18/18 |
| MP4 存在 | 18/18 |
| SRT + VTT 成对存在 | 18/18 |
| 状态 | 18/18 `prototype` |
| 证据等级 | 18/18 `L1` |
| manifest 校验 | `episodes=18; manifest validation passed` |

核验命令：

```bash
python3 langfuse/validate_manifest.py
python3 - <<'PY'
# 逐集解析 manifest 的 script/video，并检查 SRT/VTT
PY
```

## 结构性发现

1. 资产覆盖完整：每集都有脚本、MP4 和双格式字幕，因此可以作为连续播放的原型系列。
2. 证据等级没有分层：18 集全部是 `prototype / L1`。这表示有课程资产，不表示当前实例已经完成 SDK/OTEL 写入、UI/API 回读或评测闭环。
3. 迁移与运行时主题已延伸到 LF-16–18，但真实 Trace E2E 仍受项目凭据缺失和 Gateway readiness `unconfigured` 阻塞；相关结论应继续使用 `sampled-pass`、`verified`、`blocked` 的原始边界。

## 下一步最值得补的三个知识缺口

### 1. LF-19：OTEL 认证门到 Trace ID 回读

把 `401 Invalid credentials`、脱敏 OTLP payload、响应中的 Trace ID、UI/API 回读和时间戳串成一条证据链。没有受保护 key 时课程只能演示认证门与验证清单，状态保持 `BLOCKED`。

### 2. LF-20：OTEL headers、时间戳与 flush/实时性

解释 headers 如何传递认证、时间戳为何影响排序，以及 SDK/Exporter 的 flush 和最终一致性如何验证。应配最小参考代码和可复核的原始响应字段，避免把“请求发出”当成“Trace 已可见”。

### 3. LF-21：Dataset run、Score 写入与实验回读

把同一 Dataset 的 run、Score、失败样本和比较结果做成可复现闭环；需要锁定 SDK/服务端版本、脱敏输入、run/score ID 以及 UI/API 回读证据。在真实 key 和数据集不可用时仅制作脚本和证据表，不宣布评测结论。

## 不能由本次审计证明的事项

- MP4 有音视频流、时长是否均为 180 秒（需单独 ffprobe QA）。
- 官方页面当前可访问性与链接内容是否变更（见 source-link audit）。
- 当前实例的新 Trace 是否成功写入、被 Worker 消费并在 UI/API 回读。
- 数据集、Score、成本和延迟数值的真实性。

## 交接结论

系列资产完整性为 `precheckable`；内容发布证据仍为 `prototype / L1`。下一轮优先制作 LF-19/20 的课程资产，并在受保护凭据可用后再升级证据等级。
