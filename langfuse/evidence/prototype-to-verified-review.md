# prototype → verified 审阅表

## 当前可升级项

- 视频文件层面：15/15 时长、音视频流和 manifest 路径已通过。
- 来源层面：官方入口已审计，失效深链接已降级或标记待核对。
- 概念层面：LF-01–15 均有脚本/知识卡和证据边界。

## 当前不能升级项

- 没有当前微课项目的新 Trace、Dataset run 或 Score 回读。
- 没有逐集 UI/API 原始 JSON、脱敏截图和运行 commit。
- 原型画面没有展示真实调用字段，不能作为产品实测成片。
- 当前 health `OK` 不能证明写入、权限、采样、保留或备份恢复。

## 每集最小升级证据

1. 当前版本和官方 URL。
2. 受保护 Key 注入后的真实运行命令。
3. 新 Trace/Run/Score ID，以及 UI/API 同 ID 回读。
4. 脱敏原始 JSON、截图、输入输出和失败样本。
5. 对应 git commit、评分/比较条件和口播断言审查。

缺一项保持 `prototype/L1` 或 `blocked`。
