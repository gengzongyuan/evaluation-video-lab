# LF-07 v2 播放器接入前置门

## 目标

LF-07 主题为 Generation 的模型、token usage、延迟和成本。接入播放器前必须同时通过媒体门、字幕门和事实边界门；示意数字不能冒充当前实例测量。

## 媒体门

- [ ] `langfuse/videos/LF-07-cost-latency-v2.mp4` 存在且非空。
- [ ] 时长约 180 秒，分辨率 1080×1920，视频 H.264、音频 AAC。
- [ ] `volumedetect` 的 mean/max volume 均不是 `-inf`。
- [ ] 在 0、15、30、60、120、165 秒抽帧，至少 3 个不同画面哈希；镜头应推进 model、usage、start/end、latency、cost 或 unknown。
- [ ] 视频不是固定单画面，画面中的示意数字必须有 `prototype / L1` 或等价边界标记。

## 字幕门

- [ ] `langfuse/captions/LF-07-v2.srt` 和 `.vtt` 均非空。
- [ ] SRT 使用 `HH:MM:SS,mmm`，VTT 使用 `HH:MM:SS.mmm`；15 秒镜头不能误写成 15 分钟。
- [ ] 文件能以 UTF-8 解码，无 `��` 等乱码。
- [ ] 字幕逐镜对应旁白，正确区分 token usage、start/end、latency、provider 价格配置和 `unknown`。

## 内容与证据门

- [ ] 讲清 Generation 的 model、input/output、usage、start/end 和 latency 字段，并区分等待时间与模型调用时间。
- [ ] 成本只在 usage 完整、provider/价格配置和计算口径明确时讨论；缺字段写 `unknown`，不得自行补数字。
- [ ] 对照比较必须固定输入、模型、参数、网络条件和样本；一次本地 Trace 不能推导长期平均延迟、成本或整体效率。
- [ ] 不把 observability 文档或示意 JSON 当作当前项目已成功写入或回读的证明。
- [ ] 当前没有安全项目 key 时，真实 Generation 回读、usage/cost 核对和运行比较保持 `BLOCKED`。
- [ ] 真实运行升级前保存脱敏 Generation JSON、model、usageDetails、start/end、cost 或 unknown、provider/价格配置、Trace/Observation ID、实例/SDK 版本、运行日期和 SHA-256 清单。

## 验证命令

```bash
python3 langfuse/scripts/check_video_quality.py \
  langfuse/videos/LF-07-cost-latency-v2.mp4 \
  --subtitle langfuse/captions/LF-07-v2.srt \
  --subtitle langfuse/captions/LF-07-v2.vtt
python3 langfuse/validate_manifest.py
```

两条命令通过只说明媒体与路径门通过；没有受保护写入、同一 Trace/Observation 回读和逐字段核验，不能把成本、延迟或 usage 升级为 `verified`。
