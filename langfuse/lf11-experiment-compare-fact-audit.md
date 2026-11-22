# LF-11 事实审计：同 Dataset 比较 Prompt / 模型

任务：LF11-S1。官方文档核对日期：2026-11-23（Asia/Shanghai）；本集为概念课程，当前无项目 key，未执行真实运行。

## 结论

这集要守住一句话：**把两个 Prompt/模型放在同一 Dataset 版本、同一 evaluator、同一运行条件下比较；先看每个样本再看汇总。平均分升高可以掩盖关键回退。**

- 选已审查的 release run 作 baseline；新 run 不自动是已批准 baseline。
- 缺失 case 不算通过；已知失败需显式接受。
- 结论限定在这组数据、版本和条件。状态保持 `prototype / L1`。

## 官方比较口径（2026-11-23 读取）

来源：<https://langfuse.com/docs/evaluation/experiments/compare-experiments>

| 项 | 官方口径 | 边界 |
|---|---|---|
| 流程 | 先看聚合分，再查变差的 case，打开 trace 找原因 | 平均分不能掩盖关键回退 |
| baseline | 用已审查的 release run 作 baseline | 新 run 不自动是已批准 baseline |
| 同条件 | 同一 dataset 版本和 evaluator 定义；记录 commit、prompt/model 版本、evaluator 版本 | dataset 版本固定不代表模型输出确定 |
| 缺失 case | 缺失 case 不是通过 case | 不能静默丢弃 |
| 发布政策 | 先定 required-pass 或 no-regression；已知失败显式接受 | 一次比较不证明可上线 |
| 权衡 | 比较 score、cost、latency 差异 | 一次运行不推出长期 P95/SLA |

## 与现有 LF-11 审计的对齐

`lf11-fact-audit.md` 已覆盖可讲范围、最小证据包、复核。本文件补上官方 baseline、缺失 case 不算通过、发布政策先定、平均分掩盖回退的具体口径。

## 与其他 agent 的冲突

- 若有人把平均分升高写成模型更好/全面领先，与本审计冲突。
- 若有人把新 run 当已批准 baseline，或把缺失 case 当通过，与本审计冲突。

## 需要冻结的字段

- 状态：`prototype / L1`；同 Dataset 两个真实 run、Score 回读、统计显著性 `BLOCKED`。
- 同一 dataset 版本 + evaluator；baseline 用已审查 release run。
- 禁出现：内网地址、真实 key / secret、Authorization 值、登录信息、PII。

## 依据

- Compare experiments：<https://langfuse.com/docs/evaluation/experiments/compare-experiments>
- CI/CD 发布政策：<https://langfuse.com/docs/evaluation/experiments/experiments-ci-cd>

仓库内证据：`langfuse/lf11-fact-audit.md`、`langfuse/lf11-experiment-compare-lesson.md`、`langfuse/lf15-release-gate-fact-audit.md`。

## 产物与验证

独占产物：本文件。未改视频、字幕、播放器、manifest 或 `docs/quality/00-project-state.md`，未 git commit。

## 风险与下一步

没有项目 key，真实 run/回读未验证。由主 agent 把口播补上 baseline、缺失 case、发布政策口径。
