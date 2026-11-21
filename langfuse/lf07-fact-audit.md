# LF-07 成本、Token Usage 与延迟事实审计

核对范围：`lf07-cost-latency-lesson.md`、`evidence-pack-lf06-10.md`、`source-verification.md`。本审计区分官方字段语义、一次运行观察和长期性能结论。

## 可安全讲述

| 主题 | 可讲范围 | 不可推出 |
|---|---|---|
| model | Generation 可记录所用模型标识；录制时需以当前官方数据模型为准 | 当前项目本轮一定使用某模型，或模型质量更高 |
| usage | provider/SDK 返回的 input/output/total usage 可用于记录 token 消耗；字段缺失应显示 `unknown` | 缺字段时自行估算，或用单条调用代表长期成本 |
| start/end/latency | 同一事件的时间戳可计算一次调用耗时；必须说明计算口径和时区 | 一次调用推出 P95、稳定性、SLA 或“模型慢” |
| cost | 成本依赖 usage 完整性、provider、价格配置和币种/计价时间；要保存配置版本 | 没有价格配置就给出金额，或声称节省比例 |
| 对照实验 | 固定输入、模型、参数、网络和样本后才能比较一个变量 | 示意数字、不同条件的两次运行或平均数自动证明优化 |

## 当前项目状态

- 官方文档页面只能证明字段和配置方向，不能证明当前项目已成功回读 Generation。
- 当前 shell 没有安全注入 Langfuse project key/secret，因此 LF-07 的真实 Generation JSON、usage、计时点和 cost 回读保持 `BLOCKED`。
- 课程和视频继续标记 `prototype / L1`；画面中的数字必须标为示意，不能冒充实测。

## 录制前最小证据包

1. 记录 Langfuse Web、SDK/exporter、provider 版本和运行 commit。
2. 保存脱敏 Generation JSON，至少包含 model、usage（或明确 unknown）、start/end、latency 和 cost（或 unknown）。
3. 保存 provider 价格配置的来源、版本、币种和核对日期；不要把价格表快照误称为本次实际费用。
4. 对照运行固定输入、参数、模型、网络和样本；保存两次 run ID 与原始响应摘要。
5. 逐字段复��旁白、画面和字幕：任何“更快/更省/更稳定”都必须有同条件多样本数据，否则改为“本次观察”。
6. 原始响应脱敏、生成 SHA-256 清单，并记录失败样本和缺失字段。

## 发布门

- `prototype / L1`：仅有脚本、示意图或质量门通过的视频。
- `write-observed`：受保护运行收到非空写入响应，但还没有同一 Generation 的回读。
- `e2e-verified`：同一运行的 Generation JSON、时间戳、usage/cost 字段和当前版本支持的回读全部匹配。
- 缺少 key、usage、价格来源、同一 run ID 或回读响应时，保持 `BLOCKED`，不得升级。

## 验证

```bash
test -s langfuse/lf07-fact-audit.md
rg -n "unknown|BLOCKED|model|usage|latency|cost|回读" langfuse/lf07-fact-audit.md
```

本文件不声称当前实例已经完成 LF-07 的真实运行。
