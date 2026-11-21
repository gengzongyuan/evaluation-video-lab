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
