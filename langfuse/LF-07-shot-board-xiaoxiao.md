# LF-07《成本、token 与延迟》Xiaoxiao 分镜板

用途：按 `zh-CN-XiaoxiaoNeural`、`rate=-5%` 为 20 段口播制作画面。口播多长，成片就多长；禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

## 制作规则

- 20 镜使用 20 种不同构图，相邻构图不得重复。
- 每镜画面内只烧一条短字幕，完整口播保留在「口播」列。
- token、金额、耗时、趋势和模型名均为示意或留空，不是当前实例实测。
- 字段缺失统一写 `unknown`，不得自行补数或把估算当实测。
- 无内网地址、密钥、Authorization 值、PII 或真实业务输入输出。

## 20 镜分镜

| 镜 | 构图 | 时长提示 | 口播 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | 一次回答很慢，先别急着说模型慢。总等待里可能还有检索、工具和排队。 | 巨大「慢」字下方藏着检索、工具、模型三个未知段 | 回答慢，不等于模型一定慢 |
| 02 | `pipeline` | 6–10s | 从用户发出请求到看到答案，是一条完整链路。先看每一段，再看总耗时。 | 请求时间线：检索 → 工具 → 模型 → 答案，长度不标数值 | 先拆链路，再看总耗时 |
| 03 | `generation-window` | 6–10s | Generation 记录模型调用本身，可以核对模型名、开始时间、结束时间和输入输出。 | Generation 独立窗口，model / start / end / input / output 分行 | 模型调用，要单独看 Generation |
| 04 | `token-bar` | 6–10s | token usage 通常要区分输入和输出。总 token 来自哪里，要保留原始字段再解释。 | 输入与输出两段堆叠条，不填虚构数量 | token 要区分输入和输出 |
| 05 | `nested-usage` | 6–10s | 缓存、推理等更细的 usage 字段，要看供应商和 SDK 实际返回，不能凭字段名猜。 | usage 字段树，未返回的分支用虚线和 unknown | 更细的 usage，以实际返回为准 |
| 06 | `unknown-stamp` | 6–10s | 缺少 usage 就如实写 unknown。不要把字符数估算成 token，再当成真实消耗。 | 空白 usage 卡盖 unknown，旁边字符数转换公式被打叉 | 缺 usage 就写 unknown，不要补数 |
| 07 | `cost-equation` | 6–10s | 成本需要 token 用量、模型或供应商的价格配置，以及明确的计价时间。缺一项就不能给出确定金额。 | 成本公式卡：usage × price config；缺失项留空 | 成本依赖用量和价格配置 |
| 08 | `price-card` | 6–10s | 价格表快照只说明当时采用的配置，不等于本次真实账单。还要保存来源、币种和版本。 | 价格配置卡带来源、币种、日期，不写具体价格 | 价格配置不等于真实账单 |
| 09 | `volume-compare` | 6–10s | token 更多，也不能单独推出回答更好或更差。用量和质量是两条不同的证据。 | 左侧 token 条，右侧质量评分卡，中间无因果箭头 | token 多少，不直接等于质量好坏 |
| 10 | `timestamp` | 6–10s | 一次调用的延迟，可以按同一事件的开始和结束时间计算，但必须说清口径和时区。 | 同一事件两个时间戳相减，时区单独标注 | 延迟要说清起止点和时区 |
| 11 | `waterfall` | 6–10s | 总等待变慢时，把检索、工具、排队和模型调用画成瀑布，定位时间到底花在哪里。 | 纵向瀑布分解总耗时，所有区间写示意 | 用瀑布定位时间花在哪一步 |
| 12 | `trend-blank` | 6–10s | 一次调用只能说明这一次。P95、稳定性和 SLA 需要多次同条件数据，不能由单条 Trace 推出来。 | 单点延迟旁的趋势图完全留白，标「无多样本证据」 | 单条 Trace 推不出 P95 或 SLA |
| 13 | `control-board` | 6–10s | 比较成本或速度时，固定输入、模型、参数、网络和样本，只改一个条件。 | 控制面板五把锁，唯一变量框可切换 | 固定条件，只改一个变量 |
| 14 | `raw-json` | 6–10s | 保存脱敏原始 Generation 字段，再计算汇总。不要只留一张加工后的仪表盘截图。 | 原始 JSON 轮廓指向汇总卡，字段未知处保留 unknown | 先保存原始字段，再做汇总 |
| 15 | `ab-lanes` | 6–10s | 两次对照要保存各自 run 标识和原始响应摘要，确认样本和条件确实一致。 | A/B 两条跑道共享同一输入，run ID 仅显示脱敏占位 | 对照组也要能追回同一轮原始记录 |
| 16 | `readback-loop` | 6–10s | 验收时回读同一条 Generation，核对模型、时间戳、usage 和 cost。对不上就不能说字段已验证。 | 请求 → Generation ID → 同一条回读闭环 | 同一条 Generation 回读用量和成本 |
| 17 | `boundary-gate` | 6–10s | 没有项目权限、价格来源或回读证据，就保持 BLOCKED。health 200 不代表成本和延迟已验证。 | BLOCKED 门挡住 health / 价格表 / 单张截图 | health 200 ≠ 成本和延迟已验证 |
| 18 | `quality-balance` | 6–10s | 优化成本或速度时，还要看质量和关键失败。只减少 token，不一定得到更好的系统。 | 天平一边成本与速度，一边质量与失败样本 | 降成本、提速度，都不能牺牲质量门 |
| 19 | `stamp` | 6–10s | 本集画面是 prototype、L1 示意，不代表当前实例已经回读 Generation、usage、成本或延迟。 | PROTOTYPE / L1 印章，四个字段均标未证明 | prototype / L1：不是用量和成本实测 |
| 20 | `cta` | 6–10s | 下一集讲用户反馈：点赞和点踩怎样回到 Score，又怎样避免被一条反馈带偏？ | LF-08 预告卡：点赞、点踩连接 Score，旁边保留样本量 | 下一集：用户反馈怎样回到 Score |

## 固定构图顺序

`hook → pipeline → generation-window → token-bar → nested-usage → unknown-stamp → cost-equation → price-card → volume-compare → timestamp → waterfall → trend-blank → control-board → raw-json → ab-lanes → readback-loop → boundary-gate → quality-balance → stamp → cta`

## 字幕与旁白

- 声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`，禁止整段变速。
- 首次出现保留英文并给中文解释：Generation 模型调用、usage 用量、cost 成本、latency 延迟。
- 烧录字幕使用表中短句；SRT、VTT 使用同一时间轴，最后一条与片尾对齐。
- 不编造 token 数量、价格、金额、延迟、P95、节省比例或模型排名。

## 演示与证据边界

1. 录制时保存 Langfuse、SDK、provider 版本、运行 commit 和脱敏 Generation 原始字段。
2. 保存价格配置的来源、版本、币种和日期；价格表不等于实际费用。
3. 对照运行固定输入、参数、模型、网络和样本，保留 run 标识与失败样本。
4. 缺 usage、价格来源、同一 ID 或回读证据时保持 `BLOCKED`。
5. 当前文件只定义概念课画面，不证明当前实例成本、用量或延迟已验证。

## 官方来源（录制当天复核）

- Observability：https://langfuse.com/docs/observability
- 数据模型：https://langfuse.com/docs/observability/data-model
