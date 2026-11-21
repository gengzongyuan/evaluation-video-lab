# LF-05 v2 播放器接入前置检查

本文件是 LF-05「Dataset 与可重复实验」快切样片加入播放器和课程索引前的门禁。它只定义媒体和证据入口，不把脚本或示意画面当成真实 Dataset run。

## 必须存在的文件

- `langfuse/videos/LF-05-dataset-v2.mp4`
- `langfuse/captions/LF-05-v2.srt`
- `langfuse/captions/LF-05-v2.vtt`
- `langfuse/lf05-v2-qa.md`
- `langfuse/lf05-fact-audit.md`

## 媒体门

- MP4 时长为约 180 秒（质量门默认容差 ±1 秒）。
- 视频为 1080×1920、H.264；音频为 AAC 且 `volumedetect` 的 mean/max 不能是 `-inf`。
- 至少有 12 个约 15 秒镜头；在 0、15、30、60、120、165 秒抽帧时至少有 3 个不同画面哈希。
- SRT 与 VTT 非空、UTF-8 可读、时间码使用秒级格式，例如 `00:00:15,000` 或 `00:00:15.000`，不能把 15 秒写成 `00:15:00`。
- 字幕中的 Dataset、item ID、run、Score、Prompt v1/v2 和 `BLOCKED` 必须与旁白一致。

推荐命令：

```bash
python3 langfuse/scripts/check_video_quality.py \
  langfuse/videos/LF-05-dataset-v2.mp4 \
  --subtitle langfuse/captions/LF-05-v2.srt \
  --subtitle langfuse/captions/LF-05-v2.vtt
```

## Dataset 证据门

可以讲：固定输入、稳定 item ID、同一 Dataset 的两次 run、只改变一个变量、保留失败样本和运行参数，有助于复现比较。

当前不能讲成已验证事实：本项目已经成功创建 Dataset、已完成 Dataset run、某个 Prompt 或模型得分更高、成本/延迟已经改善，或实验结果具有普遍代表性。

若要把本集从 `prototype / L1` 升级，至少需要受保护运行的脱敏证据包：

1. Dataset 名称、版本、item 数量、稳定 item ID 和脱敏输入摘要；
2. Prompt/model/参数版本，以及两次 run 的 run ID 和运行时间；
3. 每个 item 的原始输出、Score、失败样本和评分规则；
4. 同一 Dataset、同一评分规则下的对照结果与统计口径；
5. SDK/实例版本、运行 commit、成本/延迟字段来源和回读响应；
6. 原始响应脱敏、敏感信息审计与 SHA-256 清单。

缺少项目 key、run ID、Score 回读或同条件对照时，状态保持 `BLOCKED`，播放器只能标为 `prototype / L1`。

## 接入结论

只有文件、媒体门、字幕审计和证据边界全部通过，才可在 `player/index.html`、`series-index.md` 和必要时 `manifest.json` 中登记 LF-05 v2。播放器链接可证明文件可访问，不能证明 Dataset run 或实验回读成功。
