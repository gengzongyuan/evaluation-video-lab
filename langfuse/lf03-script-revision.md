# LF-03 安全口播修订版：Span 和 Generation

状态：prototype script；当前实例未重跑，不把历史结构讲成当前新结果。

| 时间 | 口播 | 画面 |
|---|---|---|
| 0–15s | “看到一棵调用树，不代表每个节点都记录对了。今天只回答：普通步骤和模型调用，为什么要分开？” | 调用树先模糊，再高亮 Span / Generation |
| 15–45s | “检索、解析、路由，是流程步骤；模型请求是 Generation。类型的意义，是让你知道这一步发生了什么。” | 四张类型卡；标注‘概念示意’ |
| 45–90s | “先画真实顺序：Trace 包住一次工作单元，Span 记录普通处理，Generation 记录模型调用。父子关系跟着真实调度走。” | Trace → Span → Generation 树；箭头标父节点 |
| 90–125s | “验收不要只看 UI。记下 Trace ID，再按 ID 回读 type、name、parentObservationId、input/output 和 usage。没有 usage 就写 unknown。” | UI 与 API JSON 对照 |
| 125–155s | “本轮证据边界要说清楚：当前实例 health 是 4.79.0，但项目 Key 没有安全注入，所以没有把新 Trace 说成已跑通。” | 绿卡 health；黄卡历史；红卡 BLOCKED |
| 155–180s | “下一步是用脱敏项目 Key 重跑一条真实调用树，再把这张类型卡和 API 回读一起放进视频。” | 录制清单 + 下一集预告 |

官方来源：<https://langfuse.com/docs/observability/data-model>、<https://langfuse.com/docs/observability/best-practices>。
