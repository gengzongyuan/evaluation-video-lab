# LF-14 事实审计：SDK 与服务端版本锁定

任务：LF14-S1。官方文档及包元数据核对日期：2026-11-22（Asia/Shanghai）。

## 结论

这集最值得讲的是：**先把服务端和 SDK 的版本配对，再锁定整份运行环境**。锁版本能提高复现与回滚能力，但不能单独证明 Trace 写入、异步消费或回读成功。

`latest` 不是一个可复现的版本号。Langfuse Server、Python SDK、JS/TS SDK 和 CLI 是不同组件，不能假设它们共用同一版本号。`v4`、`v5`、`v6` 也指不同组件的大版本，不能混为一谈。

## 官方能力与可讲述范围

| 主题 | 官方支持的口径 | 不能由此推出 |
|---|---|---|
| 当前 SDK 主线 | SDK 概览列出 Python SDK v5、JS/TS SDK v6 | 任意老项目都能直接升级，或所有集成均支持同一套 API |
| 兼容性 | Server 与 SDK 独立编号；server major 的目标是支持当前及前一个 SDK major，但每个 SDK major 也有最低 server 版本；v4 迁移有例外 | 两位版本号相同才兼容，或所有旧 SDK 永久兼容新 server |
| 自托管当前配对 | 官方矩阵写明：Python SDK v5、JS/TS SDK v6 要求自托管 server >= 4.59.0 | 已记录的历史 server 4.79.0 就能证明当前项目已完成写入 |
| 运行时要求 | 兼容性文档写明 Python SDK v5 要求 Python 3.11+；JS/TS SDK v6 要求 Node.js 22+ | 只装 SDK 就满足全部框架、OTel exporter 和应用依赖 |
| 公共 API | server 的 major 变化可能涉及基础设施、公共 API 或参数变更；升级应查矩阵和升级指南 | 一个 health 200 证明所有 API、参数及读取路径不变 |
| 锁文件 | 把精确 SDK/CLI/runtime、依赖锁文件及 hash 记录进证据包，是复现与排障方法 | 官方规定必须采用某一个包管理器，或 hash 能替代行为测试 |

官方页面中的“当前/GA”是核对日的文档状态，不是本项目已安装或已验证的状态。后续发布前应重新读取这些页面，不要把本次快照当永久结论。

## 对旧 LF-14 脚本的修订

- 保留：`health` 只用于读取版本/健康信号；记录 SDK、CLI、runtime、lockfile hash 和文档日期；不把 `latest` 当版本。
- 增加：先区分 Cloud 与自托管。Cloud 的服务端由平台管理；自托管应查对应兼容性矩阵。
- 增加：明确当前主线是 Python SDK v5 / JS/TS SDK v6，以及自托管 server >= 4.59.0、Python 3.11+ / Node.js 22+ 的官方要求。
- 增加：升级前先查对应迁移指南，不直接复制旧 quickstart。旧的 `/docs/sdk` 已不能替代当前 SDK 与兼容性文档。
- 收紧：单独锁定版本、比对 hash 或获取 health 响应，都不构成真实 Trace 链路验收。

## 建议演示步骤（示意，未在本项目执行）

1. 从脱敏部署记录读取 server 版本，区分 Cloud / self-hosted。
2. 打开兼容性矩阵，选择 SDK major，确认 server 最低版本和 runtime 要求。
3. 在隔离环境安装一个明确版本，保留生成的 lockfile；不在生产项目演示无约束升级。
4. 记录 SDK、CLI、Python/Node、操作系统、server 版本、Git commit 和 lockfile SHA-256。
5. 使用受保护的项目凭据运行官方 quickstart；记录 Trace ID，flush/shutdown 后读取同一 ID 核对。
6. 升级时先在隔离环境跑最小写入和回读，再按项目回归方案逐步推进。

版本核对命令示例（录制时执行并保存原始输出；不是本任务的已执行结果）：

```bash
python --version
python -c "from importlib.metadata import version; print(version('langfuse'))"
node --version
npm ls @langfuse/tracing --depth=0
npx @langfuse/cli --version
shasum -a 256 <实际项目的锁文件>
```

Python 项目可明确写出例如 `langfuse==<核对后精确版本>`；JS/TS 项目可写 `@langfuse/tracing@<核对后精确版本>`。CLI 的 major 与 SDK 不等同，不能用 SDK 版本代替 CLI 实测版本。

## 本次可回指的版本快照

仅用于后续选题和示范，不代表项目已安装或运行通过：

| 来源 | 2026-11-22 读取结果 | 证据边界 |
|---|---|---|
| `https://pypi.org/pypi/langfuse/json` | `langfuse` 最新发布元数据为 `5.2.0`；`requires_python` 为 `>=3.11,<4.0` | 包仓库当时元数据，不是本机安装记录 |
| `https://registry.npmjs.org/@langfuse/tracing/latest` | `@langfuse/tracing` latest 为 `6.1.1`；`engines.node` 为 `>=22` | 包仓库当时元数据，不是本机安装记录 |

若后续制作采用这些精确版本，仍须在隔离环境实际安装、锁定、运行并保存证据；不能仅凭上述元数据宣称成功。

## 当前实例与不可证明范围

- 历史材料记录过 self-hosted server `4.79.0` 和健康端点观察；本次没有重新请求该实例，也没有读取当前部署、Worker、数据库或对象存储状态。
- 当前任务没有安全项目 key，没有安装 Langfuse SDK/CLI，没有发起 Trace 写入、flush、Worker 消费确认或 UI/API 回读。
- 因此项目环境配对、Trace ID 回读、升级无回归、实时性、usage/cost 一致性和生产可用性全部保持 `BLOCKED` / 未验证。
- 任何视频和字幕只能标 `prototype / L1`；不得出现内网地址、项目 key、secret、Authorization、登录信息或 PII。

## 发布门与最小证据包

- 至少保存带时间的 server/SDK/CLI/runtime 原始输出、锁文件及 hash、官方文档 URL/核对日期、隔离环境安装日志。
- 至少一条受保护的真实写入→flush→回读记录，包含可复核的 Trace ID 和脱敏 payload；没有则 `BLOCKED`。
- 升级演示要包含升级前基线、升级后最小回归、失败输出和回滚版本；不能用示意图代替。
- 脚本、口播、画面、字幕对版本的描述一致；旧版“版本已固定”不能包装成“当前运行已验证”。

## 官方来源（2026-11-22 实际读取）

- SDK 概览：<https://langfuse.com/docs/observability/sdk/overview>
- 总兼容性与 Cloud/自托管区别：<https://langfuse.com/docs/compatibility>
- 自托管版本及兼容性矩阵：<https://langfuse.com/self-hosting/upgrade/versioning>
- SDK 升级指南入口：<https://langfuse.com/docs/observability/sdk/upgrade-path>
- 自托管入口：<https://langfuse.com/self-hosting>
- 包元数据（辅助版本快照，非行为证据）：<https://pypi.org/pypi/langfuse/json>、<https://registry.npmjs.org/@langfuse/tracing/latest>

## 审计结论

LF-14 可以按“版本配对 → 精确锁定 → 最小 Trace 回读”的顺序制作。官方版本与兼容性陈述已有来源，运行证据仍缺失。状态保持 `prototype / L1`，不能升级成熟度或声称当前实例已验证。
