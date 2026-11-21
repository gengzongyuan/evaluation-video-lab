# 首轮验收

状态：in_progress。

已通过：系列定位、两条脚本、生产模板、证据等级、风险禁区均已落文件。

待通过：事实核验单、口播精修、生产看板汇合；仓库提交与远端创建；静态验收。

验收结论只能是“可拍摄视频包”，不能写成“已完成视频”。

## 验证记录（2026-11-21）

- 静态文件检查：通过；README、三份首轮内容资产均为非空。
- 内容关键词检查：通过；扫描到 43 条关键内容证据（结果、证据、CTA、时间轴、示意与证据等级）。
- Git 版本控制：通过；commit `48e1c47` 已推送 `origin/main`。
- GitHub 远端：通过；仓库为 https://github.com/gengzongyuan/evaluation-video-lab

## 可播放视频原型验收

- [x] `videos/video-01-model-rankings-prototype.mp4` 存在，180 秒，9:16
- [x] `videos/video-02-minimal-eval-prototype.mp4` 存在，180 秒，9:16
- [x] 两条视频均含中文旁白音轨
- [x] 两条视频均标记为 prototype / L1，未冒充最终发布成片
- [ ] 真实录屏、证据卡、字幕和失败样本仍待下一轮制作

## Langfuse 微课第一批

- [x] 课程地图覆盖 20 集，由浅入深，并为每集登记官方 URL。
- [x] LF-01 至 LF-06 已有约 3 分钟脚本、演示步骤和事实边界。
- [x] LF-01 已生成 180 秒可播放中文旁白原型，状态 `prototype` / `L1`。
- [ ] LF-01 的真实 SDK、UI 截图和 Trace 运行日志尚未补齐。

## Langfuse LF-02 Trace

- [x] 当前实例 health endpoint 返回 `OK / 4.79.0`。
- [x] LF-02 证据记录区分官方概念、历史 API 回读和当前实例未重跑状态。
- [x] LF-02 180 秒旁白视频原型已生成，标记 `prototype / L1`。
- [ ] 当前项目 Secret、SDK 写入、UI 回读和新 Trace ID 尚未完成；正式产品演示保持 `BLOCKED`。

## Langfuse LF-03 Span/Generation

- [x] 类型卡、脚本修订版和可执行演示计划已落库。
- [x] LF-03 180 秒旁白视频原型已生成，状态 `prototype / L1`。
- [ ] 当前实例 Span/Generation/Tool 调用树尚未用新 Trace ID 回读；正式演示保持 `BLOCKED`。

## Langfuse LF-04–06

- [x] LF-04 Prompt 管理、LF-05 Dataset、LF-06 Evaluation/Score 知识卡已写入。
- [x] LF-04 已生成 180 秒视频原型，状态 `prototype / L1`。
- [ ] LF-05 Dataset run 与 LF-06 Score 写入/回读仍待真实项目 Key 和 SDK/API 运行。

## Langfuse LF-07–09

- [x] 成本/延迟、用户反馈、生产治理三集知识卡已写入。
- [x] LF-07 已生成 180 秒视频原型，状态 `prototype / L1`。
- [ ] LF-08 反馈 Score 写入、LF-09 生产采样/脱敏/权限运行证据仍待真实环境验证。

## Langfuse LF-10–12

- [x] Agent 调用树、Prompt/模型对比实验、异常 Trace 排障闭环知识卡已写入。
- [x] LF-10 已生成 180 秒视频原型，状态 `prototype / L1`。
- [ ] LF-11 同 Dataset 双 run 与 LF-12 真实排障回归仍待项目证据验证。

## Langfuse LF-13–15

- [x] 自托管、版本锁定、发布门禁三集知识卡已写入。
- [x] LF-13 已生成 180 秒视频原型，状态 `prototype / L1`。
- [ ] LF-14 当前 SDK/API 组合与 LF-15 实际发布演练仍待后续验证。

## Langfuse 系列索引

- [x] LF-01–15 已汇总到 `langfuse/series-index.md`。
- [x] `manifest.json` 已从 6 集扩展为 15 集，并核对每个视频路径。
- [x] 脚本、知识卡和视频原型状态分离；未生成视频的集数保持 `scripted`。

## Langfuse LF-01–15 视频原型覆盖

- [x] 15/15 集 manifest 均有视频路径。
- [x] 15/15 集视频文件非空，`ffprobe` 验证每条 `duration=180.000000`。
- [ ] 所有原型仍需替换真实 UI/录屏、SDK/API 回读和脱敏证据，当前只能作为 `prototype / L1`。

## 原型质量审计

- [x] 15 集 manifest、系列索引和视频文件已统一；每集视频时长为 180 秒。
- [x] 画面资产计划和发布就绪门禁已建立。
- [ ] 真实 UI/API 证据包尚未齐全，所有视频保持 `prototype / L1`。

## 证据包模板

- [x] LF-01–05、LF-06–10、LF-11–15 三组证据包模板已建立。
- [x] manifest 中 15/15 script 路径和 15/15 video 路径均存在。
- [ ] 模板尚未被真实项目运行记录填充；视频状态仍为 `prototype / L1`。

## 历史证据与当前证据分层

- [x] 历史 LAB-02 Observation 树已整理为脱敏摘要，仅用于概念教学。
- [x] 系列验证报告已写明已证明与未证明范围。
- [ ] 当前项目新 Trace/Dataset/Score 仍未取得完整证据包；所有集数保持 `prototype / L1`。

## LF-01–03 真实录制表

- [x] 已建立可直接填写的真实录制表，涵盖版本、命令、Trace/Observation ID、UI/API、脱敏和结论。
- [ ] 当前仍缺安全项目 Key 和新运行 ID，表单尚未形成 PASS 记录。

## LF-04–15 录制表与自动校验

- [x] LF-04–08、LF-09–12、LF-13–15 录制表已建立。
- [x] `python3 langfuse/validate_manifest.py` 通过：`episodes=15`、路径和证据字段完整。
- [ ] 真实运行记录仍未填入；视频保持 `prototype / L1`。

## 视频原型 QA

- [x] 15/15 视频通过音视频流、180 秒时长和 manifest 路径检查。
- [x] QA 报告已列出画面、字幕、陌生观众复述和实例证据缺口。
- [x] prototype→verified 审阅表已建立；当前无集数满足完整升级条件。

## 字幕草稿

- [x] 15/15 集均有三段式 SRT 字幕骨架和剪辑检查说明。
- [ ] 逐字听写、真实字段核对、竖屏安全区和陌生观众复述仍待成片阶段完成。

字幕校验修正：首次自检断言过严，已改为检查 15 个 SRT、每个 3 个时间轴和 180 秒结束标记；修正后的校验通过。

## 字幕播放器样片

- [x] 15/15 SRT 已转换为 WebVTT sidecar 字幕。
- [x] LF-01 浏览器播放器样片已建立，原始 MP4 未被覆盖。
- [x] 记录 FFmpeg 当前不支持字幕硬烧录，改用 sidecar 方式验证时间轴。

## 观众理解测试

- [x] LF-01–03、LF-04–15 的 30 秒复述测试表已建立。
- [x] 测试表明确不虚构结果，未执行状态为 `not_run`。
- [ ] 真实测试者复述尚未执行，不能宣称观众理解门通过。

## 课程目录

- [x] 新增 15 集静态课程目录页，链接 MP4、SRT、VTT 和状态。
- [x] 目录链接自动检查通过。

目录链接校验修正：首次校验发现相对路径错误并阻止放行；修正为 `../videos` / `../captions` 后重新验证通过，共 45 个链接。

## 当前运行环境检查

- [x] 只读检查确认 health `OK / 4.79.0`、manifest 15 集通过、视频 QA 无坏文件。
- [x] 检查确认当前 shell 没有项目 Key/Base URL；未尝试写入或伪造 Trace。
- [ ] LF-01 新 Trace 写入和 UI/API 回读保持 `blocked`，等待受保护凭据环境。

## 安全运行脚本

- [x] 新增 `langfuse/scripts/check-runtime.sh`，只检查变量存在、health 和版本，不打印 Secret。
- [x] 无凭据负向测试返回退出码 2，未泄露任何值。

## Langfuse LF-16 v4 迁移

- [x] v4 events_only、旧 API 404 和 OTEL 迁移方向已形成脚本与视频原型。
- [x] LF-16 视频通过 180 秒音视频流 QA。
- [ ] OTEL 新 Trace 写入仍待受保护项目 Key 和当前 SDK 实跑。

## LF-16 OTEL 入口探针

- [x] OTEL 入口只读/空请求探针已完成：OPTIONS 204、空 POST 401、未发送业务数据。
- [x] 迁移课已明确入口可达不等于 Trace 写入成功。
- [ ] 受保护 Key 下的 OTLP payload、Trace ID 和回读仍待执行。

## LF-16 迁移参考代码

- [x] 新增无凭据 Python SDK v5/OTEL 参考代码，并通过 `py_compile`。
- [ ] 参考代码未在当前环境运行；当前 Trace 写入仍为 BLOCKED。

## LF-17 Health/Readiness

- [x] health/readiness 差异已形成脚本、证据摘要和 180 秒视频原型。
- [ ] 运行时探针不替代 OTEL Trace 写入或 Worker/UI/API 端到端验证。

## Langfuse LF-18 Gateway readiness

- [x] Gateway health/readiness 三层判断已形成脚本、证据摘要和 180 秒视频原型。
- [ ] 未修改 Gateway 配置，未发送模型请求，相关生产链路保持 blocked/risk。
