# Xiaoxiao v3 内嵌字幕验收

核对时间：2026-11-23（Asia/Shanghai）

## 结论

不要再对 Xiaoxiao v3 做 ffmpeg subtitles 二次烧录。这些样片已经用 PIL caption_box 把旁白画进画面底部，直接打开 MP4 就能看到字幕。再烧一层会叠字。

系统默认 ffmpeg 没有 subtitles/drawtext。带 libass 的是 `/opt/homebrew/opt/ffmpeg@7/bin/ffmpeg`，只适合给没有画面字幕的旧 v2 文件补字幕。

## 已抽帧确认（第 8 秒或第 12 秒）

| 集 | 视频 | 底部字幕条 |
|---|---|---|
| LF-01 | `videos/LF-01-langfuse-overview-xiaoxiao-v3.mp4` | 可见 |
| LF-02 | `videos/LF-02-trace-xiaoxiao-v3.mp4` | 可见 |
| LF-03 | `videos/LF-03-span-generation-xiaoxiao-v3.mp4` | 可见 |
| LF-04 | `videos/LF-04-prompt-version-xiaoxiao-v3.mp4` | 可见 |
| LF-05 | `videos/LF-05-dataset-xiaoxiao-v3.mp4` | 可见 |
| LF-06 | `videos/LF-06-score-xiaoxiao-v3.mp4` | 可见 |
| LF-07 | `videos/LF-07-cost-latency-xiaoxiao-v3.mp4` | 可见 |
| LF-09 | `videos/LF-09-governance-xiaoxiao-v3.mp4` | 可见 |

独立字幕仍保留：`captions/LF-0X-xiaoxiao-v3.srt` 与 `.vtt`。LF-01 质量门：`check_natural_voice_video.py` PASS，24 个镜头，时长约 173 秒。

## 失败实验

曾用 ffmpeg@7 把 LF-01-xiaoxiao-v3.srt 再烧到 LF-01 Xiaoxiao v3 上，抽帧看到两层字幕：底部 caption bar + 画面中部大号描边字。该文件已删除，不进入播放清单。
