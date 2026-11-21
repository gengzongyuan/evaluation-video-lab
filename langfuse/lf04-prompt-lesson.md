# LF-04｜Prompt 管理、版本和 label

## 一句话结果
看完后，观众能说清为什么把 Prompt 集中管理，以及如何用版本和 label 让一次运行可追溯。

## 3 分钟结构

- 0–20s：同一段 Prompt 被散落在代码、配置和临时脚本里，出问题无法回答“用的是哪一版”。
- 20–60s：Langfuse Prompt Management 的概念：保存 Prompt、版本、标签，并从应用侧获取。
- 60–125s：演示创建 v1、修改成 v2、给版本绑定测试/生产 label，再在应用侧记录请求的版本。
- 125–160s：把 Prompt 版本和 Trace 的 metadata 对上；用同一输入比较时，先固定模型、参数和数据。
- 160–180s：决策卡：先记录版本，再谈效果；label 存在不等于效果更好。

## 证据边界

官方文档可以证明功能和字段语义，不能证明当前项目权限、当前 UI 布局或某个版本已经发布成功。当前实例没有安全注入项目 Key，因此本集先按概念演示；真实 UI/API 录制需重新运行并保存版本号、label、Trace ID 和原始输入。

来源：<https://langfuse.com/docs/prompt-management>、<https://langfuse.com/docs/prompt-management>。
