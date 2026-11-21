# Langfuse 系列验证报告

核验日期：2026-11-22（Asia/Shanghai）

## 已证明

- Langfuse 实例健康端点返回 `status=OK, version=4.79.0`。
- manifest 中 LF-01–15 的 script/video 路径全部存在。
- 15 条 MP4 均可被 ffprobe 解码，时长为 180 秒。
- 官方来源链接已做一次审计；失效深链接已降级到官方父页或当前指南入口。
- 历史 LAB-02 有脱敏的 Observation 树回读摘要，可用于概念教学。

## 尚未证明

- 当前微课项目用新项目 Key 写入的新 Trace、Dataset run 或 Score。
- 当前视频画面与真实 UI/API 回读一一对应。
- 生产采样、权限、脱敏、保留、告警和回滚已在目标部署上通过。

## 状态规则

所有视频保持 `prototype / L1`。只有在证据包的运行命令、原始回读、脱敏截图、版本和 commit 都齐全后，才允许逐集升级 `verified / L2`；不存在“全系列自动升级”。
