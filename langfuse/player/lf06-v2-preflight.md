# LF-06 v2 播放器接入前置门

## 目标

LF-06 主题为 Evaluation、Score 与失败样本。只有媒体文件、字幕、事实边界和证据记录全部齐全，才可把 v2 样片接入播放器与课程索引。

## 媒体门

- [ ] `langfuse/videos/LF-06-score-v2.mp4` 存在且非空。
- [ ] 时长约 180 秒，容差按质量脚本执行。
- [ ] 分辨率为 1080×1920，视频 H.264、音频 AAC。
- [ ] `volumedetect` 的 mean/max volume 都不是 `-inf`。
- [ ] 0、15、30、60、120、165 秒抽帧至少产生 3 个不同画面哈希。
- [ ] 视频包含不少于 12 个约 15 秒镜头，画面随评分规则、运行证据和失败样本推进。

## 字幕门

- [ ] `langfuse/captions/LF-06-v2.srt` 和 `.vtt` 均非空。
- [ ] 时间码使用 `HH:MM:SS,mmm`（SRT）或 `HH:MM:SS.mmm`（VTT）；15 秒镜头不能写成 15 分钟。
- [ ] UTF-8 可解码，无 `��` 等乱码。
- [ ] 字幕与旁白逐镜对应，准确区分 Score、evaluator、Trace/Run ID、失败样本和回读。

## 内容与证据门

- [ ] 先定义评分问题、范围、单位和空值规则，再讲写入 Score。
- [ ] 画面可展示固定 Trace 或 Dataset run、Score、原始高/低分样本和评估器版本，但示意画面必须标 `prototype / L1`。
- [ ] 明确 Score 是判断工具，不是脱离任务的真理；平均分不能替代失败样本和人工复核。
- [ ] 不把 Score API/SDK 概念文档当作当前项目已成功写入或回读的证明。
- [ ] 当前没有安全项目 key 时，真实 Score 写入、Trace/Run 回读和评测闭环保持 `BLOCKED`。
- [ ] 真实运行升级前需保存 run/trace/observation ID、score_id、value/data_type、evaluator 版本、原始样本、脱敏回读 JSON、实例/SDK 版本、时间和 SHA-256 清单。

## 验证命令

```bash
python3 langfuse/scripts/check_video_quality.py \
  langfuse/videos/LF-06-score-v2.mp4 \
  --subtitle langfuse/captions/LF-06-v2.srt \
  --subtitle langfuse/captions/LF-06-v2.vtt
python3 langfuse/validate_manifest.py
```

两条命令通过只说明媒体和路径门通过；没有受保护写入、同一 ID 回读和逐字段核验，不能升级为 `verified`。
