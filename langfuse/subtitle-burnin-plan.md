# 字幕方案

核对日期：2026-11-23（Asia/Shanghai）

## 当前正确做法

Xiaoxiao v3 渲染脚本在画帧时写入底部字幕条（caption_box）。用户打开 MP4 就能看见字幕，同时保留独立 SRT/VTT。

不要对 Xiaoxiao v3 再跑 ffmpeg subtitles 滤镜，会叠两层字。

## 仅适用于旧 v2（画面里没有字幕条）

系统 PATH 里的 ffmpeg 8.1.2 没有 subtitles/ass/drawtext。需要烧录时用：

```bash
/opt/homebrew/opt/ffmpeg@7/bin/ffmpeg -i <old-v2.mp4> \
  -vf "subtitles=filename=<file.srt>:force_style='FontName=STSong,FontSize=16,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BorderStyle=1,Outline=2,Shadow=1,Alignment=2,MarginV=90'" \
  -c:v libx264 -crf 20 -c:a copy <out-burnin.mp4>
```

烧录后必须抽帧确认只有一层字幕，并且不覆盖源文件。
