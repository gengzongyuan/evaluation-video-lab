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
