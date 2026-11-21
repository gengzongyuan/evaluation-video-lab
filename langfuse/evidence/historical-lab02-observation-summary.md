# 历史 LAB-02 Observation 回读摘要（脱敏引用）

来源：本机历史实验的 `lab02-api-evidence.html`，采集时间早于本 Langfuse 微课当前版本。此摘要只用于解释 LF-03/LF-10 的调用树概念，不作为当前实例新运行的 verified 证据。

## 可引用事实

- 一条历史 Trace 曾回读到 4 条 Observation。
- 根节点类型为 `AGENT`；其下有 `GENERATION`、`TOOL` 和另一条 `GENERATION`。
- `parentObservationId` 能把模型和工具节点挂回同一个 Agent 工作单元。
- 工具结果包含成功标记和退出码；模型节点可用于区分模型调用与工具调用。

## 不可引用为结论的内容

- 不能说这条历史 Trace 来自当前微课代码或当前 commit。
- 不能把历史 project、Trace ID、内部地址或截图直接放入公开视频。
- 不能凭这 4 条 Observation 证明 Agent 稳定性、工具安全或生产容量。
- 不能替代当前项目 Key、当前 SDK 和当前 Langfuse 版本的重新回读。

## 视频处理

画面使用抽象树或重新生成的虚构 ID；不展示原始项目名、Trace ID、工作区路径和完整输入输出。旁白必须说“历史实验摘要”或“结构示例”，并保留 L1 证据等级。
