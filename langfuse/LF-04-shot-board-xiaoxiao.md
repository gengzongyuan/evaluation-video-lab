# LF-04《Prompt 管理、版本和 label》Xiaoxiao 分镜板

用途：按 `zh-CN-XiaoxiaoNeural`、`rate=-5%` 为 20 段口播制作画面。口播多长，成片就多长；禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

## 制作规则

- 20 镜使用 20 种不同构图，相邻构图不得重复。
- 每镜画面内只烧一条短字幕，完整口播保留在「口播」列。
- Prompt 名称、版本、label、Trace ID 均为示意，不是当前实例已创建或发布的事实。
- 版本、label、SDK 字段以录制当天官方文档与部署版本为准；不得把 label 口播成质量提升。
- 无内网地址、密钥、Authorization 值、内部 Prompt 或真实用户内容。

## 20 镜分镜

| 镜 | 构图 | 时长提示 | 口播 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | Prompt 只改了一行，线上回答为什么突然变了？你先得知道：这次到底用了哪一版。 | 超大问号压住一行被修改的 Prompt，输出区出现变化标记 | Prompt 改一行，先问用了哪一版 |
| 02 | `scattered` | 6–10s | 如果提示词散落在代码、配置和临时脚本里，出问题就只能逐处翻，连差异都很难对齐。 | 三处文件碎片散落，红色问号连接不上同一版本 | 散落各处的 Prompt，很难回溯 |
| 03 | `prompt-card` | 6–10s | Langfuse 的 Prompt 管理，先把一段提示词集中保存，给它明确的名字和内容。 | 居中的 Prompt 卡：`answer-guide-demo`；正文只用脱敏变量 | 先给 Prompt 一个明确的名字和内容 |
| 04 | `version-stack` | 6–10s | 内容有变化，就形成可回指的版本。排错时看的是具体版本，不只是一个名字。 | 纵向版本卡 v1 / v2，旁注「概念示意」，不画效果分数 | 同一个 Prompt 名，也要区分具体版本 |
| 05 | `label-road` | 6–10s | label 用来指向你选择的版本，例如把测试和生产环境的入口分开。它不是效果分数。 | 岔路牌：test / production，各自指向版本卡；没有升降箭头 | label 指向版本，不代表效果更好 |
| 06 | `code-fetch` | 6–10s | 应用运行时再取回 Prompt，填入变量，再把渲染后的输入交给模型。 | 伪代码三段：获取 → 填变量 → 生成；密钥只显示环境变量占位 | 获取 Prompt → 填变量 → 交给模型 |
| 07 | `trace-link` | 6–10s | 关键不是取到就结束，而是让这次运行能回指实际使用的 Prompt 和版本。 | Trace 节点与 Prompt 版本卡用虚线连接，字段待真实回读核对 | 让这次运行回指实际 Prompt 版本 |
| 08 | `version-diff` | 6–10s | 复查两个版本时，先看文本到底改了哪里，不要先凭感觉说哪版更好。 | 左右文本差异，仅高亮一行措辞；质量栏保持空白 | 先看版本差异，再谈效果 |
| 09 | `label-warning` | 6–10s | 把 production label 指向某个版本，也不等于这个版本已经通过实验或适合上线。 | production 标签旁出现黄色警告，发布闸门仍未打开 | label 生效 ≠ 质量已验收 |
| 10 | `run-boundary` | 6–10s | 真正录制时，要锁定 Langfuse、SDK 版本和运行时间，再保存实际返回的版本与 label。 | 元数据条：版本 / SDK / 日期 / label；全部用可替换占位符 | 先锁定版本、时间和实际返回 |
| 11 | `fixed-input` | 6–10s | 想比较 Prompt，就固定同一条脱敏输入，别一版用简单题，另一版换难题。 | 同一输入卡被复制到两条跑道，样本 ID 保持一致 | 比较 Prompt，先固定同一条输入 |
| 12 | `control-grid` | 6–10s | 模型、参数和数据也要固定。只改 Prompt 版本，后面的差异才有解释的起点。 | 控制面板四行，只有 Prompt 版本允许切换，其余锁上 | 模型、参数、数据固定，只改 Prompt |
| 13 | `score-split` | 6–10s | 有了分数也别只看版本号。还要看同一批样本、同一评分规则和失败案例。 | 左版本卡，右样本与评分清单；不填虚构分数 | 分数要连同样本和评分规则一起看 |
| 14 | `rollback` | 6–10s | 发现问题时，版本记录让你知道从哪里退、退到哪一版；这只是回滚线索，不是自动恢复。 | 从当前版本指向上一版的回退箭头，审批节点保持待确认 | 版本帮助回滚，但不等于自动恢复 |
| 15 | `checklist` | 6–10s | 发布前核对 Prompt 名、版本、label、创建时间和内容摘要，缺一项就先别宣称已发布。 | 五项检查卡；缺失项用空框而非绿色全勾 | 名称、版本、label、时间、内容都要核对 |
| 16 | `not-equal` | 6–10s | 页面能打开、health 返回 200，都不能证明 Prompt 已保存、label 已生效或这次运行回指成功。 | health 200 与 Prompt 已验证之间放不等号，后者标未证明 | health 200 ≠ Prompt 已发布并回指 |
| 17 | `loop` | 6–10s | 最小证据闭环是：取回 Prompt，跑一次请求，拿到 Trace ID，再回读同一条记录核对版本。 | 四步闭环：Prompt → 请求 → Trace ID → 回读 | 用同一个 Trace ID 回读 Prompt 版本 |
| 18 | `evidence-gate` | 6–10s | 如果遇到 401、404 或字段对不上，保留原始响应并停止放行，不要拿截图补齐结论。 | 红门挡在 401 / 404 / 字段不一致前，后门保留原始记录 | 认证或字段失败，就停止放行 |
| 19 | `stamp` | 6–10s | 本集画面是 prototype、L1 示意，不代表当前实例已创建版本、修改 label 或完成 Trace 回读。 | PROTOTYPE / L1 印章，下方列出创建、label、回读均未证明 | prototype / L1：不是当前实例已发布 |
| 20 | `cta` | 6–10s | 下一集讲 Dataset：为什么同一组样本，比随手换几个问题更适合做重复实验？ | LF-05 预告卡，固定样本集图标连接两次运行 | 下一集：用同一组样本做重复实验 |

## 固定构图顺序

`hook → scattered → prompt-card → version-stack → label-road → code-fetch → trace-link → version-diff → label-warning → run-boundary → fixed-input → control-grid → score-split → rollback → checklist → not-equal → loop → evidence-gate → stamp → cta`

## 字幕与旁白

- 声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`，禁止整段变速。
- 首次出现保留英文并给中文解释：Prompt 提示词、version 版本、label 标签。
- 烧录字幕使用表中短句；SRT、VTT 使用同一时间轴，最后一条与片尾对齐。
- 不编造版本提升、成本下降、部署成功或实验胜负。

## 演示与证据边界

1. 录制前锁定官方页面、Langfuse 与 SDK 版本，按当前接口获取 Prompt。
2. 使用脱敏模板与固定输入，保存实际返回版本、label、Trace ID 和同一条回读。
3. 版本或 label 存在不等于质量更好，不等于生产部署，也不等于全链路完成。
4. 认证、字段或回读失败保持 `BLOCKED`，不得用 health、截图或历史运行替代。
5. 本文件只定义概念课画面，不证明当前实例写入、获取、发布或回读。

## 官方来源（检索日期 2026-11-23）

- Prompt Management：https://langfuse.com/docs/prompt-management
- Observability 功能：https://langfuse.com/docs/observability/features
- Python SDK：https://langfuse.com/docs/sdk/python
