# LF-03 可执行演示计划

## 实验目标
在一个脱敏项目中创建 Trace，包含一个普通 Span、一个 Generation 和（若当前 SDK 支持）一个 Tool；通过 UI 与 API 核对类型和父子关系。

## 步骤

1. 记录 Langfuse Web 版本、SDK 版本、日期和项目 ID；Key 只从受保护环境变量读取。
2. 使用固定输入，先建立 Trace。
3. 执行检索/解析占位函数，写入 Span。
4. 执行一次模型调用，写入 Generation；记录 model 和 usage，缺失记 `unknown`。
5. 若调用真实工具，使用无副作用 fixture，写入 Tool；禁止用手工 API 伪造事件。
6. flush/shutdown 后在 UI 展开树，保存脱敏截图。
7. 用 `observations list --trace-id` 或当前官方 API 等价命令回读 JSON，核对 type、name、parentObservationId、input/output、status。

## 判定

- PASS：新 Trace 可刷新；类型与真实步骤一致；父子关系正确；API 可回读；无秘密/PII。
- BLOCKED：无项目 Key、无可控工具、SDK 参数未核对或只看到历史 Trace。
- FAIL：类型错挂、重复记录、输入输出泄露或回读的 Trace 不是本次运行。

当前状态：BLOCKED（项目 Key 和当前 SDK 实跑证据缺失）。官方来源：<https://langfuse.com/docs/observability/data-model>。
