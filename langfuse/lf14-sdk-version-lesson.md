# LF-14｜SDK 与服务端版本锁定

## 一句话结果
看完后，观众能在录制前固定 Langfuse 服务端、SDK、CLI、Node/Python 和 lockfile，并记录 API 变更风险。

## 核验清单

1. 记录 Langfuse health 返回版本。
2. 记录 SDK/CLI 精确版本和包管理器 lockfile hash。
3. 保存官方文档 URL、页面标题和核对日期。
4. 用脱敏 quickstart 跑最小 Trace；API 字段变化时先更新脚本。
5. 在视频角标显示版本和日期；不把 `latest` 当作可复现版本。

## 边界

版本锁定提升可追溯性，不保证不同 provider 的 usage、cost 或 UI 完全一致；没有运行日志时只能说“示例代码”。

来源：<https://langfuse.com/docs/sdk>、<https://langfuse.com/self-hosting>。
