# 项目质量状态

- 项目：3分钟评测科普视频系列
- 模式：project + sustained-goal
- 当前阶段：需求与价值决策 / 内容生产方案
- 阶段状态：in_progress
- 当前成熟度：precheckable
- 项目 A：用户；Codex 承担 PM/TL/QA/执行
- 本轮目标：在 1.5 小时内交付至少两条可直接拍摄或剪辑的视频包，并建立可持续生产方法。

## 持续 Goal 当前轮（2026-11-22）

- LF-19、LF-20 已完成课程设计、180 秒 MP4 原型和 SRT/VTT 字幕，已登记为 `prototype / L1`；真实 OTEL 运行证据仍待补齐。
- LF-21 已完成 Dataset run、Score 写入和实验回读课程脚本，登记为 `scripted / L1`，尚未生成视频。
- LAB-02 证据审计已完成：raw 文件 JSON 解析和 SHA-256 校验通过；health/readiness 为时间点采样，OTEL 入口存在已验证，认证成功、Trace 写入、回读和实时延迟均为 `BLOCKED`。
- LF-01–LF-20 资产审计通过：20/20 有脚本、MP4、SRT 和 VTT，全部保持 `prototype / L1`；LF-21 有脚本，保持 `scripted / L1`。
- 快切 v2 样片已扩展到 LF-01–LF-03：每集 12 个约 15 秒镜头、中文旁白、非静音音频和多时间点画面变化；LF-02 字幕时间码与乱码已修复。
- 快切 v2 样片已扩展到 LF-01–LF-06；LF-06 覆盖评分规则、Score 关联、评估器版本、高低分和失败样本，媒体门通过，仍保持 `prototype / L1`。
- 快切 v2 样片已扩展到 LF-01–LF-09；LF-09 覆盖 sampling、脱敏、保留、权限、密钥轮换和告警，字幕乱码已修复，媒体门通过，仍保持 `prototype / L1`。
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
## Xiaoxiao 原速重制（2026-11-22 晚）

- 用户选定 `zh-CN-XiaoxiaoNeural`。旧 Xiaoxiao 180 秒成片被独立复核判定 FAIL：音频被拉伸、12 张卡片、无画面内字幕。
- 新样片：`langfuse/videos/LF-01-langfuse-overview-xiaoxiao-v3.mp4`，168.7 秒、24 镜、原速旁白、烧录字幕。状态仍 `prototype / L1`。
- 播放器 LF-01 已改为优先该文件。
- 未把 health 200、示意画面或媒体门写成当前实例已验证。

## Xiaoxiao 原速重制（2026-11-23）

- 用户选定 `zh-CN-XiaoxiaoNeural`，`rate=-5%`。禁止 macOS `say`，禁止把短音频拉伸到 180 秒。
- LF-01 已重渲第 4 镜乱码配音：`langfuse/videos/LF-01-langfuse-overview-xiaoxiao-v3.mp4`，173.033 秒、24 镜、画面内字幕；自然旁白门 PASS。
- LF-02：`langfuse/videos/LF-02-trace-xiaoxiao-v3.mp4`，161.003 秒、20 镜、画面内字幕；独立抽帧与自然旁白门 PASS。
- LF-03：`langfuse/videos/LF-03-span-generation-xiaoxiao-v3.mp4`，170.600 秒、20 镜、画面内字幕；独立抽帧与自然旁白门 PASS。
- LF-04：`langfuse/videos/LF-04-prompt-version-xiaoxiao-v3.mp4`，166.866 秒、20 镜、画面内字幕；独立抽帧、自然旁白门与独立复核 PASS。
- LF-05：`langfuse/videos/LF-05-dataset-xiaoxiao-v3.mp4`，173.071 秒、20 镜、画面内字幕；主 agent 抽帧与自然旁白门 PASS。
- LF-07：`langfuse/videos/LF-07-cost-latency-xiaoxiao-v3.mp4`，176.233 秒、20 镜、画面内字幕；独立抽帧与自然旁白门 PASS。
- LF-06：`langfuse/videos/LF-06-score-xiaoxiao-v3.mp4`，171.266 秒、20 镜、画面内字幕；主 agent 抽帧与自然旁白门 PASS。
- LF-09：`langfuse/videos/LF-09-governance-xiaoxiao-v3.mp4`，182.876 秒、20 镜、画面内字幕；主 agent 抽帧与自然旁白门 PASS。时长由旁白决定，略超 180 秒。
- LF-08：`langfuse/videos/LF-08-feedback-xiaoxiao-v3.mp4`，173.166 秒、20 镜、画面内字幕；主 agent 抽帧与自然旁白门 PASS。
- LF-10：`langfuse/videos/LF-10-agent-tree-xiaoxiao-v3.mp4`，181.760 秒、20 镜、画面内字幕；主 agent 抽帧与自然旁白门 PASS。第 1 镜 11.376 秒略超 10 秒，保持原速。
- LF-11：`langfuse/videos/LF-11-compare-xiaoxiao-v3.mp4`，170.900 秒、20 镜、画面内字幕；主 agent 抽帧与自然旁白门 PASS。第 14 镜 10.032 秒略超 10 秒，保持原速。
- LF-12：`langfuse/videos/LF-12-debug-regression-xiaoxiao-v3.mp4`，173.633 秒、20 镜、画面内字幕；主 agent 抽帧与自然旁白门 PASS。第 2 镜 10.008 秒略超 10 秒，保持原速。
- 播放器已优先链接 LF-01 到 LF-12 的 Xiaoxiao 原速版。状态仍全部 `prototype / L1`。
- 未把 health 200、示意 ID、媒体门或截图写成当前实例 Trace/Dataset/Score 写入或回读已验证。
