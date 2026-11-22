# LF-18《Gateway Readiness》Xiaoxiao 分镜板

用途：按 `zh-CN-XiaoxiaoNeural`、`rate=-5%` 为 20 段口播制作画面。口播多长，成片就多长；禁止拉伸到固定 180 秒。状态保持 `prototype / L1`。

## 制作规则

- 20 镜使用 20 种不同构图，相邻构图不得重复。
- 每镜画面内只烧一条短字幕，完整口播保留在「口播」列。
- Gateway 状态若引用历史探针，必须标采样时间；不代表此刻状态。
- 无内网地址、密钥、Authorization 值、登录信息、PII 或真实 provider 配置。

## 20 镜分镜

| 镜 | 构图 | 时长提示 | 口播 | 画面 | 烧录字幕 |
|---:|---|---|---|---|---|
| 01 | `hook` | 6–10s | Gateway health 返回 200，ready 却是 503 unconfigured。进程活着，为什么还不能接模型流量？ | health 200 与 ready 503 强烈对照，模型流量被拦住 | health 200，不代表 Gateway 已就绪 |
| 02 | `liveness` | 6–10s | `/health` 是 liveness，只检查进程能否服务 HTTP，不检查 web、provider 或路由依赖。 | liveness 卡只包住 Gateway 进程，依赖在框外 | Gateway health 不检查依赖 |
| 03 | `shutdown-card` | 6–10s | 官方还说明，关闭期间 health 也可能继续 200。它用来表达进程状态，不用于业务验收。 | shutdown 状态旁 health 仍为 200，业务门仍关闭 | 关闭期间的 health，也不是业务通过 |
| 04 | `ready-config` | 6–10s | `/ready` 关注配置就绪，核心是 web URL 和 service key。缺配置时返回 503 unconfigured。 | ready 配置卡只显示 web URL / service key 占位符 | ready 先检查 web URL 和 service key |
| 05 | `diagnosis-boundary` | 6–10s | unconfigured 指向配置未就绪，但不是完整诊断。具体缺哪项、路由对不对，还要受保护环境核对。 | 未配置卡展开多个待核对项，不武断指定根因 | unconfigured 是风险信号，不是完整根因 |
| 06 | `secret-boundary` | 6–10s | 排查 service key 时只看是否存在、是否有效，不要在视频里展示真实值或完整配置。 | service key 值完全隐藏，只显示检查状态 | 检查凭据，不展示真实密钥 |
| 07 | `route-map` | 6–10s | provider 和路由是另外一层。web URL、service key 配好，也不能自动证明每个模型路由正确。 | web/provider/route 三层路由图，各自待验证 | 配置就绪，不等于每个路由正确 |
| 08 | `no-call` | 6–10s | 最关键的一点：ready 不会真的调用 web 或 provider。它适合做流量准入，不适合当请求验收。 | ready 检查旁没有真实调用箭头，只有配置检查 | Gateway ready 不会发真实模型请求 |
| 09 | `false-ready` | 6–10s | 所以即使 ready 200，web 或 provider 不可达时，真实请求仍可能失败。 | ready 200 与 provider 失败同时出现，不构成矛盾 | ready 200，也可能请求失败 |
| 10 | `load-balancer` | 6–10s | readiness 更适合告诉负载均衡器能不能接流量。不要把负载均衡的门当成业务成功的门。 | 负载均衡器接流量，业务请求验证另起一条路径 | 流量准入门 ≠ 业务成功门 |
| 11 | `model-chain` | 6–10s | 如果模型请求走 Gateway，就要单独测应用、Gateway、provider 和响应回传的完整链路。 | 应用 → Gateway → provider → 响应闭环 | 模型流量走 Gateway，就要单独测全链路 |
| 12 | `trace-separation` | 6–10s | Langfuse Trace 写入和 Gateway 模型转发是两件事。当前 Trace 写入不依赖 Gateway。 | Trace 写入链路与 Gateway 模型链路两条泳道分开 | Trace 写入和 Gateway 转发不能混验 |
| 13 | `request-evidence` | 6–10s | 真实请求要保存脱敏请求摘要、模型与路由、响应状态和时间，用同一请求标识回查日志。 | 请求证据卡，字段均为脱敏占位 | 用同一请求标识核对响应和日志 |
| 14 | `error-log` | 6–10s | provider 不可达、认证失败或路由错误，往往要回到单次请求和 Gateway 日志定位。 | 单次请求卡连接错误日志摘要，敏感头全部遮盖 | 真实错误要回到单次请求和日志 |
| 15 | `metric-gate` | 6–10s | Gateway 未 ready 时，不能把这次模型请求的成本、延迟或质量说成生产证据。 | 成本、延迟、质量三张指标卡停在风险门前 | Gateway 未就绪，指标不能当生产证据 |
| 16 | `remediation` | 6–10s | 修复时在受保护环境核对 web URL、service key 和路由，保存变更摘要，不直接在生产盲改。 | 受控变更卡连接配置检查与审计，真实值隐藏 | 在受保护环境修复并留下变更摘要 |
| 17 | `retest-loop` | 6–10s | 修复后先看 ready，再发一条真实模型请求，最后回查响应和日志。三步不能省成一步。 | 配置修复 → ready → 真实请求 → 日志回查闭环 | ready、真实请求、日志回查三步齐全 |
| 18 | `rollback` | 6–10s | 配置修复失败要能回到上一版明确配置，并重测模型链路。回滚也不是 health 200 就结束。 | 配置回滚后重新进入真实请求验证 | 回滚后仍要重测真实模型链路 |
| 19 | `stamp` | 6–10s | 本集画面是 prototype、L1 示意，没有修改 Gateway 配置，也没有发送真实模型请求。 | PROTOTYPE / L1 印章，配置修复与模型请求均标未执行 | prototype / L1：未修复配置，未发模型请求 |
| 20 | `cta` | 6–10s | 下一集讲 OTEL 认证与回读：认证门通过以后，怎样证明新 Trace 真的能按 ID 读回来？ | LF-19 预告卡：认证 → Trace ID → 同 ID 回读 | 下一集：OTEL 认证通过后的回读证据 |

## 固定构图顺序

`hook → liveness → shutdown-card → ready-config → diagnosis-boundary → secret-boundary → route-map → no-call → false-ready → load-balancer → model-chain → trace-separation → request-evidence → error-log → metric-gate → remediation → retest-loop → rollback → stamp → cta`

## 字幕与旁白

- 声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%`，禁止整段变速。
- 首次出现保留英文并给中文解释：Gateway 网关、health 存活检查、ready 就绪检查、provider 模型供应商。
- 烧录字幕使用表中短句；SRT、VTT 使用同一时间轴，最后一条与片尾对齐。
- 不伪造配置修复、模型请求、provider 状态、成本、延迟或生产结论。

## 演示与证据边界

1. health 是进程存活，ready 是配置就绪；两者都不是真实模型请求。
2. unconfigured 指向 web URL/service key 类配置缺失，但不是完整根因。
3. ready 不调用 web/provider；真实链路必须单独发请求并回查日志。
4. Trace 写入与 Gateway 转发分开验证；未 ready 时模型指标保持风险。
5. 当前文件只定义概念课画面，不证明当前 Gateway 配置或模型链路已验证。

## 官方来源（录制当天复核）

- AI Gateway：https://langfuse.com/self-hosting/configuration/ai-gateway
- Docker Compose：https://langfuse.com/self-hosting/deployment/docker-compose
