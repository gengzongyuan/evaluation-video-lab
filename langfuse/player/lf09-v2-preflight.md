# LF-09 v2 播放器接入前置门

## 适用范围

本文件用于审核 `LF-09-governance-v2.mp4` 是否可以接入播放器和课程索引。它只定义媒体与内容边界，不把示意画面当成当前部署已安全或已合规的证明。

## 必须存在的文件

- `langfuse/videos/LF-09-governance-v2.mp4`
- `langfuse/captions/LF-09-v2.srt`
- `langfuse/captions/LF-09-v2.vtt`
- `langfuse/lf09-v2-qa.md`
- `langfuse/lf09-fact-audit.md`

## 媒体门

- 时长约 180 秒，允许误差不超过 1 秒。
- 分辨率 1080×1920，视频 H.264，音频 AAC。
- 音频 `mean_volume` 和 `max_volume` 均不能为 `-inf`。
- 0、15、30、60、120、165 秒抽帧至少有 3 个��同画面哈希。
- 至少 12 个约 15 秒镜头；每镜有标题、治理动作、清单字段或状态变化。
- SRT/VTT 非空、UTF-8 可读，时间码按 15 秒镜头核对，不能出现乱码。

## 内容与隐私门

- sampling 只讲可见性、成本和错误覆盖之间的取舍；不能用示意比例声称当前实例的采样率或成本节省。
- 脱敏画面不得出现 key、secret、Authorization、PII、完整 prompt、cookie、内网地址或可回溯业务数据。
- retention 只讲配置和核对项；没有当前部署配置、时间戳和审计记录时，不能说“已经按周期删除”。
- 权限和密钥轮换必须以清单或官方能力说明呈现，不得说当前项目已完成权限审计或轮换。
- 告警画面必须标为示意，不能把健康检查、历史截图或静态日志说成当前生产告警。
- 旁白和字幕必须保留 `prototype / L1`；不能把“配置能力”扩大为“部署安全”或“合规通过”。

## 运行证据门

只有在受保护环境保存以下材料后，才可考虑提升证据等级：

1. 采样规则版本、脱敏规则和测试输入输出摘要。
2. retention、权限、TLS、密钥轮换的当前配置和审计时间。
3. 一条脱敏 Trace 的写入、回读和访问记录。
4. 告警触发、通知和从告警回到 Trace/版本/失败样本的证据。
5. 原始响应、命令、运行版本和 SHA-256 清单。

当前无项目 key 或完整部署审计时，sampling/脱敏/retention/权限/告警的真实验证保持 `BLOCKED`，视频状态保持 `prototype / L1`。

## 接入前命令

```bash
python3 langfuse/scripts/check_video_quality.py \
  langfuse/videos/LF-09-governance-v2.mp4 \
  --subtitle langfuse/captions/LF-09-v2.srt \
  --subtitle langfuse/captions/LF-09-v2.vtt
python3 langfuse/validate_manifest.py
rg -n "prototype / L1|BLOCKED|sampling|脱敏|retention|权限" \
  langfuse/lf09-v2-qa.md langfuse/lf09-fact-audit.md \
  langfuse/captions/LF-09-v2.srt
```

质量门通过只表示媒体可播放和边界文字存在；播放器接入仍需主 agent 审核来源、字幕同步和脱敏结果。
