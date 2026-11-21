# v2 快切样片目录 QA

核对范围：LF-01-v2、LF-02-v2。

- 两条视频均为 prototype / L1，不能表述为真实 Langfuse UI 或 Trace 写入证��。
- 播放器已提供 v2 MP4 和 SRT/VTT 链接，旧版原型保留为对照。
- LF-03 等后续样片必须通过 `langfuse/scripts/check_video_quality.py` 后再接入。

验证：

```bash
test -s langfuse/videos/LF-01-langfuse-overview-v2.mp4
test -s langfuse/videos/LF-02-trace-v2.mp4
test -s langfuse/captions/LF-01-v2.srt
test -s langfuse/captions/LF-02-v2.srt
```
