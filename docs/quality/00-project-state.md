# 项目质量状态

- 项目：3分钟评测科普视频系列
- 模式：project + sustained-goal
- 当前阶段：需求与价值决策 / 内容生产方案
- 阶段状态：in_progress
- 当前成熟度：precheckable
- 项目 A：用户；Codex 承担 PM/TL/QA/执行
- 本轮目标：在 1.5 小时内交付至少两条可直接拍摄或剪辑的视频包，并建立可持续生产方法。

## 持续 Goal 当前轮（2026-11-22）

- LF-19、LF-20 已完成课程设计稿，仍待视频、字幕和真实 OTEL 运行证据后才能登记为可播放集数。
- LAB-02 证据审计已完成：raw 文件 JSON 解析和 SHA-256 校验通过；health/readiness 为时间点采样，OTEL 入口存在已验证，认证成功、Trace 写入、回读和实时延迟均为 `BLOCKED`。
- LF-01–LF-18 资产审计通过：18/18 有脚本、MP4、SRT 和 VTT，全部保持 `prototype / L1`。
- 本轮验证命令：`python3 langfuse/validate_manifest.py` 通过；在 `langfuse/evidence/raw/` 执行 `shasum -a 256 -c SHA256SUMS-2026-11-22.txt` 全部通过。

## 已完成证据

- 系列定位、受众、选题准入和两条选题：`content/agent-v01-topic.md`
- 两条约 3 分钟脚本、时间轴、口播、画面和 CTA：`content/agent-v02-scripts.md`
- 生产模板、证据卡、L0-L3 证据等级和发布门：`content/agent-v03-format.md`
- 第二批事实核验、口播精修、生产看板待汇合。

## 本轮验收门

- [x] 两条视频脚本存在，时长约 3 分钟
- [x] 每条有一句话结果、最小实验、画面、CTA、证据边界
- [x] 明确示意数据不能冒充实测结论
- [ ] 事实核验单与生产看板完成汇合
- [ ] Git 仓库初始化、提交并推送到 GitHub
- [ ] 运行静态验收命令并记录结果

## 阻塞与风险

- 尚无真实实验数据，因此不能发布具体模型排名或优劣结论。
- 尚未拍摄、配音、剪辑或平台发布；本轮交付口径为“可拍摄视频包”。
- GitHub 仓库名和是否公开采用默认：`evaluation-video-lab`、公开仓库；如远端同名已存在则改用带日期后缀。

## 下一层问题

哪类真实评测证据最能提升完播、收藏和评论后的复现实验率？下一轮用真实样本、30秒复述测试和发布数据验证。

## Langfuse 下一层问题

在不暴露项目凭据的前提下，如何为 LF-19/LF-20 补齐脱敏 OTLP payload、Trace ID 回读和实时性证据，使课程从 `prototype / L1` 进入可复核的 `verified` 层？

## 验证更新

- 静态验收已通过。
- GitHub 仓库已创建并推送，commit `48e1c47`。
- 首轮阶段仍保持 `in_progress`：真实拍摄与事实核验尚未完成。

## 当前新增证据

- 两条 180 秒可播放竖屏视频原型已生成：`videos/`。
- `ffprobe` 验证两条视频均为 `duration=180.000000`；视频清单记录状态为 `prototype`、证据等级 `L1`。
- 事实核验包已由子任务提交：`a97b8ed`，位置为 `docs/fact-check/video-fact-check.md`。

## Goal 切换：Langfuse 微课

- 当前长期 Goal：把 Langfuse 官方知识体系持续转译成由浅入深的 3 分钟视频系列。
- 当前阶段：课程地图与第一批脚本，状态 `in_progress`。
- 本轮并行任务：LF-01 课程地图、LF-02 入门脚本、LF-03 评测/实验脚本。
- 本轮质量门：官方来源可回指、每集有一句话结果、演示步骤和事实边界；未运行内容不得宣称已验证。

## Langfuse 微课第一批结果

- 课程地图：`langfuse/curriculum-map.md`，20 集。
- 脚本：`langfuse/scripts-beginner.md`（LF-01–03）、`langfuse/scripts-evaluation.md`（LF-04–06）。
- manifest：`langfuse/manifest.json`，登记 6 集脚本及官方来源。
- 可播放原型：`langfuse/videos/LF-01-langfuse-overview-prototype.mp4`，ffprobe 验证 180 秒。
- 当前成熟度：`precheckable`；真实实例演示尚未完成。

## 第二轮 Langfuse 资产

- 来源审计：`langfuse/source-audit.md`。
- LF-02 录制清单：`langfuse/recording-checklist-trace.md`。
- LF-03/LF-04 演示实验：`langfuse/demo-experiments.md`。
- 2026-11-21 已请求本地实例 `/api/public/health?failIfDatabaseUnavailable=true`，返回 JSON 且实例记录为 4.79.0；Trace 写入与 UI 查询仍待真实 SDK 运行验证。

## Langfuse LF-03 结果

- 类型卡：`langfuse/lf03-type-card.md`。
- 安全口播：`langfuse/lf03-script-revision.md`。
- 演示计划：`langfuse/lf03-demo-plan.md`。
- 视频原型：`langfuse/videos/LF-03-span-generation-prototype.mp4`，ffprobe 验证 180 秒。
- 当前状态：`prototype / L1`；真实调用树仍等待项目 Key 与 SDK 运行证据。

## Langfuse 系列索引结果

- 课程索引：`langfuse/series-index.md`，LF-01–15。
- manifest 已登记 15 集；其中 7 集有可播放原型，8 集保持脚本状态。
- 本轮验证：manifest episode 数量为 15；所有登记视频文件存在且非空。
