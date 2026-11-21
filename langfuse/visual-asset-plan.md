# LF-01–15 画面与字幕资产计划

每集原型当前是旁白+底图；升级前必须按下表替换为真实画面，所有截图脱敏并保留原始证据。

| 集数 | 必须补的画面 | 字幕重点 |
|---|---|---|
| LF-01 | 项目首页、Trace 列表、最小 SDK 代码 | 记录发生了什么，不等于质量已证明 |
| LF-02 | Trace 详情、Trace ID、API 回读 | accepted ≠ completed |
| LF-03 | Span/Generation/Tool 调用树、字段对照 | type/name/parentObservationId |
| LF-04 | Prompt v1/v2、label、Trace metadata | 先记录版本，再比较效果 |
| LF-05 | Dataset item、run、原始输出 | 同一输入才能比较 |
| LF-06 | Score 规则、正负样本、失败卡片 | 总分不能藏掉红线 |
| LF-07 | Generation usage、latency、cost 字段 | 缺失写 unknown，不猜数字 |
| LF-08 | 反馈入口、Trace、Score 回写 | 反馈不等于总体满意度 |
| LF-09 | Sampling、脱敏、权限、保留配置 | 可见性、成本、隐私一起看 |
| LF-10 | Agent/检索/工具/Generation 树 | 调用树跟真实调度走 |
| LF-11 | 两个 run 的同 item 对照表 | 同 Dataset、同规则、看失败样本 |
| LF-12 | 异常 Trace、修复 commit、回归结果 | 发现→定位→修复→回归 |
| LF-13 | Web/Worker/DB/对象存储架构和 health | 页面可开不等于链路通过 |
| LF-14 | 版本、lockfile、health JSON、文档日期 | 不用 latest 录制 |
| LF-15 | 证据卡、脱敏前后、release checklist | 没有证据就保持 blocked |

## 通用字幕规则

- 关键字段用等宽字体；每行不超过 14 个汉字。
- 所有示意数字显示“示意”；真实数字显示版本、日期和来源。
- `prototype / L1` 角标固定出现，直到 UI/API 证据包通过。
