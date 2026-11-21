# LAB-02 凭据与敏感信息审计

审计日期：2026-11-22（Asia/Shanghai）  
范围：当前工作区 `deepseek harnes`、内嵌仓库 `evaluation-video-lab`、当前分支全部 Git 历史、LAB-02 HTML/PNG 素材。

## 结论

未发现可直接使用的 Langfuse 项目 Secret、OpenAI key、AWS access key、Bearer token、密码明文、私钥或 `.env` 凭据。当前仓库可以继续保留演示材料，但截图和部署交接文档含有需要限制传播的实例和工作区信息，不应按“公开无敏感信息”处理。

## 证据

- 对工作区文本和 `evaluation-video-lab` 全部受版本控制文本执行了模式扫描：`sk-lf-*`、`pk-lf-*`、`sk-*`、`AKIA*`、`Bearer ...`、私钥头、常见 `SECRET/TOKEN/API_KEY/PASSWORD=...` 均无命中。
- 对 `evaluation-video-lab` 全部 Git 历史执行 `git grep` 扫描，无上述凭据模式命中；当前历史只有文档和视频原型，没有发现被删除后仍留在历史中的密钥。
- [lab02-api-evidence.html](../../lab02-api-evidence.html) 只含项目名、Trace/Observation ID 和脱敏结果，不含项目 key 或 Authorization header。
- `LANGFUSE_DEPLOYED_INSTANCE_172.16.33.136.md` 明确写明密码、API Secret、加密密钥和私钥不写入文档；正文未发现这些值。

## 需要限制传播的信息

1. `lab02-langfuse.png` 与 `lab02-langfuse-fixed.png` 显示自托管项目名 `tree_eval`/`local_agent`、真实 Trace ID、Observation 树、调用时间、模型/Token/延迟摘要，以及完整的 Codex 输入输出片段；其中��见本机工作区路径和部分内部上下文。这些不是凭据，但属于业务和环境信息。
2. `LANGFUSE_DEPLOYED_INSTANCE_172.16.33.136.md` 暴露内网 IP、SSH 用户名、端口、服务拓扑、容器名、卷路径和健康端点。该文档适合私有运维交接，不适合公开仓库或公开文章。
3. 部署文档中的 `mysecret`、`postgres` 等只出现在“不要沿用默认值”的说明或占位模板中，不能当成泄露凭据；发布前仍应确认没有把模板误当实际配置。

## 处置建议

- 发布截图前裁掉项目名、Trace ID、工作区路径、完整 prompt/output、内部时间和 token 数；必要时重新生成完全虚构的演示数据。
- 部署交接文档放在私有运维空间；若需公开教程，只保留通用架构和占位符，并把 `172.16.33.136`、SSH 用户、内部端口和路径替换为示例值。
- 正式运行前继续使用环境变量或受限凭据文件注入 key；不要把真实 `.env`、备份、日志或命令输出加入 Git。若未来扫描发现真实 key，应立即吊销/轮换，再清理历史。

