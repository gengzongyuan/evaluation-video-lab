# LF-11 v2 播放器接入前置门

## 媒体门

- [ ] MP4 非空，约 180 秒（默认容差 ±1 秒）。
- [ ] 1080×1920 竖屏，H.264 视频和 AAC 音频。
- [ ] 音频 `volumedetect` 的 mean/max 不为 `-inf`。
- [ ] 0、15、30、60、120、165 秒抽帧至少有 3 个不同画面；至少 12 个约 15 秒镜头。
- [ ] SRT/VTT 均非空、UTF-8 可读，时间码对应镜头，不得把 `00:00:15` 写成 15 分钟。

## 内容与证据门

- [ ] 画面按冻结 Dataset、Prompt/模型条件、run A/B、逐 item 输出、失败分类、汇总和结论边界推进。
- [ ] 明确冻结 Dataset、模型/参数、评分规则、运行日期和版本；只改变一个比较变量。
- [ ] 对比结论限定在本次 Dataset 和条件，不使用“全面领先”“一定更好”等无证据断言。
- [ ] 说明逐 item 样本、失败类型和运行波动，不能只展示平均分。
- [ ] 如果出现示意分数、延迟、成本或差异，画面和字幕必须标注示意，不能称为当前实例实测。
- [ ] 没有项目 key 时，不得声称真实 run、Score 写入、实验回读或统计显著性已经完成；保持 `prototype / L1` 和 `BLOCKED`。
- [ ] 任何真实运行证据至少应包含 Dataset 版本、run ID、Prompt/模型版本、评分规则、逐 item 输出、失败样本、回读响应和运行 commit。

## 接入命令

```bash
python3 langfuse/scripts/check_video_quality.py \
  langfuse/videos/LF-11-experiment-compare-v2.mp4 \
  --subtitle langfuse/captions/LF-11-v2.srt \
  --subtitle langfuse/captions/LF-11-v2.vtt
python3 langfuse/validate_manifest.py
```

两个命令通过只说明媒体和清单路径可用；它们不能替代真实 Dataset run、Score 回读、统计检验或人工内容验收。
