# LF-01～LF-05 官方来源核验

核验日期：2026-11-21（Asia/Shanghai）

| 集数 | 官方页面 | HTTP | 用于视频的证据 | 不能由页面证明 |
|---|---|---:|---|---|
| LF-01 | https://langfuse.com/docs | 200 | Langfuse 的官方产品/文档入口；用作术语和功能导航 | 本地实例已部署、任何具体版本行为 |
| LF-02 | https://langfuse.com/docs/sdk/python | 200 | Python SDK 接入路径；脚本需按页面当前 API 写法 | 当前环境凭据、网络或项目权限一定可用 |
| LF-03 | https://langfuse.com/docs/observability/data-model | 200 | Trace、Observation 及父子关系的数据模型说明 | 某条本地 Trace 的真实字段；需用实例回读 |
| LF-04 | https://langfuse.com/docs/observability/features | 200 | Observability 功能导航和可观测字段方向 | UI 当前布局在所有版本一致 |
| LF-05 | https://langfuse.com/docs/observability | 200 | Observability 总览；用于解释从请求到排障的链路 | 具体项目的延迟、token 或成本数值 |

## 拍摄前执行

1. 打开页面并保存当天截图或页面存档；记录 Langfuse Web 与 SDK 版本。
2. 运行最小示例，保存命令、原始输出、Trace ID 和 UI 截图；密钥不进入视频或仓库。
3. 将“官方页面说明”与“本地实例观察”分成两张证据卡，避免把文档能力写成已验证运行结果。
4. 页面返回非 200、API 示例变更或实例字段不一致时，脚本状态降为 `needs-review`，不得继续生成最终视频。
