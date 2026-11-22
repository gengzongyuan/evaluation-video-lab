# LF-14《SDK 与 Server 版本锁定》Xiaoxiao 分镜板

用途：按 `zh-CN-XiaoxiaoNeural`、`rate=-5%` 为 20 段口播制作画面。口播多长，成片就多长；禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

## 制作规则

- 20 镜使用 20 种不同构图，相邻构图不得重复。
- 每镜画面内只烧一条短字幕，完整口播保留在「口播」列。
- 文档版本号是核对日快照，不是本项目已安装或已运行版本。
- 锁定版本只提高复现能力，不证明 Trace 写入、Worker 消费、回读或升级无回归。
- 无内网地址、密钥、Authorization 值、登录信息或 PII。

## 20 镜分镜

| 镜 | 构图 | 时长提示 | 口播 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | SDK 写着最新版，server 也能打开，为什么接入还是失败？先别升级，先把版本关系核对清楚。 | “最新版”标签与页面打开并排，中间接入链路断开 | 最新版和页面打开，都不能证明兼容 |
| 02 | `cloud-selfhost` | 6–10s | 先区分 Cloud 和自托管。Cloud 的 server 由平台管理，自托管则要核对自己的部署版本。 | Cloud / self-hosted 两条路径，版本责任边界不同 | Cloud 和自托管，版本责任不一样 |
| 03 | `three-numbers` | 6–10s | Server、SDK 和 CLI 是三个独立编号的组件。不要把它们的版本号写成同一个数字。 | 三张独立版本卡：server / SDK / CLI，互不相等 | Server、SDK、CLI 不共用版本号 |
| 04 | `sdk-mainline` | 6–10s | 核对日官方主线是 Python SDK v5、JS/TS SDK v6。它们只是文档快照，不是你项目已安装的版本。 | 两条主线卡盖文档日期，项目安装状态标未检查 | 官方主线不等于项目已安装版本 |
| 05 | `matrix` | 6–10s | 自托管要查兼容性矩阵。核对日文档中，这两条 SDK 主线要求的最低 server 是 4.59.0。 | 矩阵行标最低 server >= 4.59.0，并盖核对日期 | 最低 server 版本要查兼容矩阵 |
| 06 | `runtime` | 6–10s | 运行环境也不能漏。官方核对日口径是 Python 3.11 及以上、Node.js 22 及以上。 | Python / Node 两张 runtime 卡，日期与来源随画面保留 | SDK 之外，还要核对 runtime 要求 |
| 07 | `compatibility` | 6–10s | 兼不兼容，不是看两个版本号一不一样，而是看 server major、SDK major 和最低版本要求。 | 兼容性判断图：major + minimum，而非等号 | 兼容看版本关系，不看数字相同 |
| 08 | `migration-warning` | 6–10s | v4 迁移还有单独注意事项。升级前必须读对应迁移指南，不要直接复制旧 quickstart。 | v4 迁移警告卡指向升级指南，旧示例被暂停使用 | 大版本迁移先读对应升级指南 |
| 09 | `exact-version` | 6–10s | 安装时写精确版本，不要只写 latest。版本号必须来自当天核对与隔离环境实测。 | `langfuse==<核对后版本>` 与包名占位，latest 被打叉 | 用精确版本替代 latest |
| 10 | `lockfile-hash` | 6–10s | 保留依赖锁文件和 SHA-256，同时记录操作系统、runtime、Git commit 和安装日期。 | 锁文件与 SHA-256 卡连接运行环境清单 | 锁文件、hash 和运行环境一起保存 |
| 11 | `isolated-install` | 6–10s | 在隔离环境安装并保存日志，不要直接在生产项目里无约束升级。安装成功也不等于链路成功。 | 隔离环境安装终端与生产环境隔开 | 先隔离安装，不在生产直接试升级 |
| 12 | `docs-pair` | 6–10s | 版本矩阵回答能不能配，升级指南回答怎么迁。两类文档都要在录制当天重新读取。 | 兼容性矩阵与升级指南双页并排 | 版本配对和迁移步骤要分别核对 |
| 13 | `baseline` | 6–10s | 升级前先保存可运行的最小基线：原版本、原始输出、Trace ID 和回读结果。 | 升级前基线卡固定版本与最小 Trace 证据 | 升级前先留下可运行基线 |
| 14 | `quickstart` | 6–10s | 再用受保护项目凭据运行当前官方 quickstart。公开画面只显示脱敏输入和环境变量占位。 | quickstart 流程卡，凭据完全隐藏，Trace ID 用占位符 | 用当前 quickstart 做最小运行验证 |
| 15 | `readback-loop` | 6–10s | flush 或 shutdown 后，用同一个 Trace ID 回读，核对输入、输出、时间和状态。 | 写入 → flush → Trace ID → 同一条回读闭环 | 同一个 Trace ID 回读核对 |
| 16 | `health-boundary` | 6–10s | health 200 只能说明当时端点响应，不能证明新 Trace 写入、Worker 消费或读取路径不变。 | health 卡与三条未证明项分开 | health 200 ≠ SDK 链路已验证 |
| 17 | `blocked-gate` | 6–10s | 没有项目权限、锁文件、真实写入或同 ID 回读，就保持 BLOCKED，不要拿文档版本补运行结论。 | BLOCKED 门挡住版本文档与截图，运行证据缺失 | 缺运行证据，就保持 BLOCKED |
| 18 | `rollback` | 6–10s | 升级失败要回到明确的旧版本，并重跑最小回归。回滚版本也要可复现，而不是再写 latest。 | 新版本 → 固定旧版本 → 最小回归，路径可回指 | 回滚也要固定版本并重跑回归 |
| 19 | `stamp` | 6–10s | 本集画面是 prototype、L1 示意，不代表本项目已安装这些版本，或升级和回读已通过。 | PROTOTYPE / L1 印章，安装、升级、回读均标未证明 | prototype / L1：不是版本升级已验证 |
| 20 | `cta` | 6–10s | 下一集讲发布门禁：视频能播放和实验能上线，为什么是两套完全不同的验收？ | LF-15 预告卡：媒体门 / 实验门并列，互不替代 | 下一集：视频发布门和实验发布门 |

## 固定构图顺序

`hook → cloud-selfhost → three-numbers → sdk-mainline → matrix → runtime → compatibility → migration-warning → exact-version → lockfile-hash → isolated-install → docs-pair → baseline → quickstart → readback-loop → health-boundary → blocked-gate → rollback → stamp → cta`

## 字幕与旁白

- 声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`，禁止整段变速。
- 首次出现保留英文并给中文解释：SDK 开发工具包、server 服务端、runtime 运行环境、digest 镜像摘要。
- 烧录字幕使用表中短句；SRT、VTT 使用同一时间轴，最后一条与片尾对齐。
- 所有版本快照附核对日期，不说成项目当前安装或永久兼容保证。

## 演示与证据边界

1. 核对 Cloud/自托管、server/SDK/CLI/runtime 版本和对应迁移指南。
2. 隔离安装精确版本，保存锁文件、hash、日志、commit 与日期。
3. 升级前保存基线，升级后用当前 quickstart、flush 和同一 Trace ID 回读。
4. 缺项目权限、真实写入或回读保持 `BLOCKED`；health 与文档不能替代。
5. 当前文件只定义概念课画面，不证明项目安装、升级、回滚或运行成功。

## 官方来源（录制当天复核）

- SDK 概览：https://langfuse.com/docs/observability/sdk/overview
- 兼容性：https://langfuse.com/docs/compatibility
- 自托管版本矩阵：https://langfuse.com/self-hosting/upgrade/versioning
- SDK 升级指南：https://langfuse.com/docs/observability/sdk/upgrade-path
