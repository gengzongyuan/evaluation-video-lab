# LF-10｜多步骤 Agent 的可观测调用树

## 一句话结果
看完后，观众能把 Agent、检索、工具和模型调用放进一棵可解释的 Trace tree，并知道哪里需要回读验证。

## 演示

1. 固定一个脱敏用户问题。
2. 创建 Trace，记录 Agent 工作单元。
3. 将检索/解析记为普通步骤，将模型调用记为 Generation，将工具调用记为当前 SDK 支持的 Tool 类型。
4. 保存每个节点的 `type/name/parentObservationId/input/output/status`。
5. 用 UI 和 API 对照调用树，检查没有孤立、重复或错挂节点。

## 边界

一棵完整的调用树能帮助排障，不自动证明任务质量、工具安全或所有分支都被采样。当前项目 Key 缺失，正式回读保持 BLOCKED。

来源：<https://langfuse.com/docs/observability>、<https://langfuse.com/docs/observability/data-model>。
