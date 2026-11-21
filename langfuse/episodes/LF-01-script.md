# LF-01｜Langfuse 到底记录什么？

状态：scripted；证据等级：L1（概念讲解，需实例截图升级）

## 一句话结果

看完后，观众能用一棵三层树解释 Langfuse：一次请求是 Trace，里面的步骤是 Observation，模型调用是 Generation；评分是挂在结果上的 Score。

## 180 秒时间轴

| 时间 | 口播 | 画面 | 证据边界 |
|---|---|---|---|
| 0–10s | “你看到的不是一堆日志，而是一棵能排障的调用树。” | 一条请求从根节点展开 | 动画为概念示意 |
| 10–35s | “先看 Trace：它代表一次用户请求或业务流程。” | 根节点：trace | 具体命名随 SDK/项目约定 |
| 35–75s | “Trace 里面是 Observation：步骤、工具、检索或模型调用。” | 子节点逐个展开 | 以官方 Data Model 页面为准 |
| 75–110s | “模型调用通常是 Generation；这里才看模型、输入输出、token 和耗时。” | Generation 卡片高亮 | 数值必须来自实例或明确标示示意 |
| 110–135s | “最后是 Score：把人工、代码或评测器对结果的判断挂回来。” | Score 标签回连 Trace | 本集不比较具体模型分数 |
| 135–165s | “排障时先问三件事：是哪次请求、哪一步慢、哪次生成错。” | 三问卡片 | 三问是本系列工作法，不是官方硬性口径 |
| 165–180s | “下一集，我们实际接入第一条 Trace。” | LF-02 预告 | 需准备可运行 SDK 示例 |

## 演示准备

- 官方来源：<https://langfuse.com/docs>、<https://langfuse.com/docs/observability/data-model>
- 实例素材：保存一条脱敏 Trace 的 ID、父子 Observation 关系和 UI 截图。
- 不展示：API key、用户原文中的个人信息、内部 URL 或未核验成本数字。

## 发布前门禁

- [ ] 术语与官方 Data Model 页面核对。
- [ ] 动画中的 Trace/Observation/Generation/Score 与截图字段逐项对应。
- [ ] 若没有实例截图，标题和口播必须保留“概念演示”措辞。
- [ ] 30 秒复述测试：观众能说出 Trace 与 Generation 的区别。
