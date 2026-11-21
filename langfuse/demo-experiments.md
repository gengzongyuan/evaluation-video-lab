# LF-03 / LF-04 可执行演示实验

## 实验 A：Span 与 Generation 的父子关系

**问题**：如何把“检索/工具步骤”和“模型调用”分开观察？

**输入**：一条脱敏用户问题；一个固定的检索占位步骤；一次模型调用。

**步骤**：

1. 创建一个 Trace。
2. 在 Trace 下创建一个 Span，名称为 `retrieve_context`，记录输入和返回文档数量。
3. 在同一父级或 Span 下创建一个 Generation，记录模型名、输入、输出和 usage（若 SDK/模型返回）。
4. flush 后在 UI 展开调用树。

**预期观察**：UI 能区分普通步骤和模型 Generation；父子关系能帮助定位时间与失败位置。

**不能证明**：一次调用不能证明稳定性、模型质量、成本准确性或所有 SDK 版本行为。

**来源**：https://langfuse.com/docs/observability/data-model 、https://langfuse.com/docs/sdk

## 实验 B：Prompt 版本与标签

**问题**：如何把 Prompt 从代码常量变成可追踪版本？

**输入**：一个不含密钥和隐私的 Prompt，两个文本版本，测试/生产标签约定。

**步骤**：

1. 在 Prompt 管理中创建初始版本，并记录版本号与创建时间。
2. 修改一个可见规则，创建第二个版本。
3. 按当前官方文档给版本绑定测试或生产 label。
4. 用 SDK/API 获取指定 label，记录返回的版本号；不要只截图管理页。

**预��观察**：代码请求的是 label/版本，输出可回指 Prompt 版本。

**不能证明**：版本标签存在不等于业务效果提升；必须用同一 Dataset 和评分规则另做实验。

**来源**：https://langfuse.com/docs/prompt-management 、https://langfuse.com/docs/prompt-management/features/version-control

## 发布前证据

- 保存 SDK 版本、Langfuse 版本、运行日期、原始输入/输出和脱敏后的 UI 截图。
- 任何“更好”“更快”“节省”字样必须有同条件对照；否则改成“本次观察”。
- 若 API 字段或 UI 与脚本不一致，优先按当前官方文档改脚本，并记录差异。
