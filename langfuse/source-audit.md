# LF-01–06 官方来源审计

核对日期：2026-11-21（北京时间）。官方文档用于证明产品概念和配置方式；本地实例记录用于证明 `172.16.33.136` 的部署事实。两者不能互相替代。

| 集数 | 官方来源 | 录制前必须核对 | 当前状态 |
|---|---|---|---|
| LF-01 | https://langfuse.com/docs 、https://langfuse.com/docs/sdk | SDK 安装命令、初始化字段、当前 UI 首页 | 文档已登记；实例演示待录 |
| LF-02 | https://langfuse.com/docs/observability/overview 、https://langfuse.com/docs/observability/data-model | Trace 创建方式、Trace/Observation 字段、服务端版本 | 文档已登记；本地 Web health 已有 4.79.0 证据 |
| LF-03 | https://langfuse.com/docs/observability/data-model 、https://langfuse.com/docs/sdk | Span/Generation 当前命名、父子关系、结束/flush 行为 | 文档已登记；代码需按当前 SDK 运行 |
| LF-04 | https://langfuse.com/docs/prompt-management 、https://langfuse.com/docs/prompt-management/features/version-control | Prompt 获取 API、版本号、label 语义、缓存行为 | 文档已登记；发布前核对实例权限 |
| LF-05 | https://langfuse.com/docs/datasets 、https://langfuse.com/docs/evaluation/experiments | Dataset item 字段、run/experiment 入口、结果写回字段 | 文档已登记；需用脱敏样本实跑 |
| LF-06 | https://langfuse.com/docs/evaluation/overview 、https://langfuse.com/docs/observability/features/scores | Score 类型、数值/分类约束、绑定对象、UI 展示 | 文档已登记；需保存原始 score 请求与 UI 结果 |

## 版本风险

- 本地实例记录为 Langfuse 4.79.0，现场文档写明 Web health 为 `status=OK, version=4.79.0`；拍摄时仍需重新请求健康端点。
- 官方文档是滚动更新页面；每次录制必须保存 URL、页面标题、核对日期和 SDK 版本。
- 不把 runbook 中的部署事实扩写为 SDK/API 已验证；没有运行日志的字段只能写“待录制核对”。
