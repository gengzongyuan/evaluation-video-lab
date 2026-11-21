# LF-12｜从异常 Trace 到修复和回归

## 一句话结果
看完后，观众能把异常发现、Trace 定位、修复、回归和告警串成一个闭环。

## 闭环

1. 发现异常：错误率、延迟、成本或用户反馈触发信号。
2. 定位 Trace：按时间、版本、session 或 request ID 找到真实运行。
3. 分类失败：模型、工具、数据、权限、配置或环境。
4. 修复并记录 commit：保持输入、版本和验证条件可追溯。
5. 用 Dataset/回归样本重跑；保留修复前后失败样本。
6. 设定告警与回滚门槛，观察修复是否引入新问题。

## 放行门

没有原始 Trace、失败样本和修复后回归证据，状态只能是 `needs-review` 或 `blocked`；一张漂亮的 Dashboard 截图不能替代闭环证据。

来源：<https://langfuse.com/docs/observability/features/dashboards>、<https://langfuse.com/docs/evaluation/experiments>。
