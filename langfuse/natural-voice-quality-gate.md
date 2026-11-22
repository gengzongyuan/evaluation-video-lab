# 原速旁白质量门

日期：2026-11-22（Asia/Shanghai）

## 为什么另写一门

`check_video_quality.py` 和 `qa_fastcut_video.py` 只证明“能播、有 AAC、大约 180 秒、抽几帧有变化”。它们会放行：

- 把 129 秒 Xiaoxiao 原速音频拉伸到 180 秒；
- SRT 跟慢速轴、VTT 仍停在原速轴；
- 12 张 15 秒信息卡；
- 没有画面内字幕。

本门只拦制作缺陷，不证明 Langfuse 写入、Worker 或回读。状态保持 `prototype / L1`。

## 失败条件

1. 封装时长与音频流时长相差超过 0.35 秒。
2. 片尾在最后一段有声之后还有超过 1.5 秒静音。
3. SRT 与 VTT 最后时间码相差超过 80ms，或任一字幕结束早于视频超过 400ms。
4. 缺少 SRT/VTT、出现替换符 `U+FFFD`，或把秒写成 `15:00` 那种 15 分钟时间码。
5. 提供 `--shots` 时，唯一镜头 id 少于 18。

不把 `ffmpeg select=gt(scene,0.08) >= 18` 当作硬门。深色卡片切镜经常检不出场景变化。没有 `--shots` 时输出 `SHOTS_SKIP`，不因此 FAIL。

## 命令

```bash
python3 langfuse/scripts/check_natural_voice_video.py \
  langfuse/videos/LF-01-langfuse-overview-xiaoxiao-v3.mp4 \
  --subtitle langfuse/captions/LF-01-xiaoxiao-v3.srt \
  --subtitle langfuse/captions/LF-01-xiaoxiao-v3.vtt \
  --shots langfuse/build/lf01-xiaoxiao-v3/timeline.json
```

对照应 FAIL 的拉伸版：

```bash
python3 langfuse/scripts/check_natural_voice_video.py \
  langfuse/videos/LF-01-langfuse-overview-xiaoxiao.mp4 \
  --subtitle langfuse/captions/LF-01-xiaoxiao.srt \
  --subtitle langfuse/captions/LF-01-xiaoxiao.vtt
```

## 2026-11-23 实测

- 拉伸版：退出码 `1`，`FAIL`。VTT 比视频早结束 50.560 秒，SRT/VTT 最后时间码相差 50.356 秒。
- v3 原速版：退出码 `0`，`PASS`。封装与音频时长相差 0.036 秒，尾部静音 0.000 秒，SRT/VTT 相差 0.000 秒，24 个唯一镜头 id。
- `python3 -m py_compile langfuse/scripts/check_natural_voice_video.py` 通过。

旧片的 0.112 秒音视频封装差和 0.877 秒尾部静音没有超过各自阈值；它仍因字幕时间轴错误被拦下。原速旁白、画面内字幕和真人听感还需要内容与画面复核，不能只凭本门宣称整条课程已验收。
