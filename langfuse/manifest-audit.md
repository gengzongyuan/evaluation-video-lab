# Langfuse 微课清单审计

核验日期：2026-11-22（Asia/Shanghai）

## 当前发现

- `langfuse/manifest.json` 当前只登记 LF-01～LF-06（6 集）。
- 仓库已经存在 LF-07～LF-15 的脚本资产，以及 LF-01、02、03、04、07、10、13 的视频原型；这些新增资产尚未全部登记到 manifest。
- manifest 中 `video` 字段写的是相对仓库路径 `langfuse/videos/...`，但脚本从 `langfuse/manifest.json` 读取时应以仓库根目录为基准，工具需统一路径约定。
- LF-02/LF-03/LF-04 的 `claim_level` 为 L1，且证据备注明确写了 project key / fresh write pending；视频标题和封面不能使用“已验证生产能力”等升级性表述。

## 放行前修复清单

- [ ] 将 LF-07～LF-15 的脚本、视频原型和来源字段补入 manifest，或明确标为 backlog。
- [ ] 统一路径约定：`langfuse/videos/...` 表示仓库根相对路径，并在 README 写明。
- [ ] 每集补 `version_checked_at`、`runtime_evidence`、`status` 和 `claim_level`。
- [ ] 只有完成当前实例写入、UI/API 回读并保存脱敏证据的集数，才能从 `prototype` 升级为 `verified`。
- [ ] 对不存在的脚本路径、视频路径执行脚本检查；缺失项保持 `blocked`，不靠文件名推断完成。

## 建议的下一个深挖问题

当前实例缺少项目 key 时，如何安全地完成 LF-02/LF-03 的真实 Trace 写入与 API/UI 回读，而不把凭据、内部地址或历史样例误当成新证据？
