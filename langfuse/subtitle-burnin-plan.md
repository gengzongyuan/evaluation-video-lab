# 字幕烧录方案（LF-01）

## 结论
当前系统 ffmpeg 8.1.2 不包含 `subtitles`/`ass`/`drawtext` 视频滤镜，无法在本机直接把 SRT 烧录进 MP4；不能把“外挂 SRT”冒充“视频内字幕”。

## 已确认资产
- 原视频：`videos/LF-01-langfuse-overview-v2.mp4`
- 字幕：`captions/LF-01-v2.srt`、`captions/LF-01-v2.vtt`
- 中文字体可用：`STSong`、`Kaiti SC`

## 推荐命令（在带 libass 的 ffmpeg 环境执行）
```bash
ffmpeg -i LF-01-langfuse-overview-v2.mp4 \
  -vf "subtitles=LF-01-v2.srt:force_style='FontName=STSong,FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H80000000,BorderStyle=1,Outline=2,Shadow=1,Alignment=2,MarginV=90'" \
  -c:v libx264 -crf 20 -c:a copy LF-01-langfuse-overview-v2-burnin.mp4
```

## 字幕样式
白字、黑色描边、底部居中、90px 下边距；每段字幕控制在两行以内。独立 SRT/VTT 仍需保留，便于播放器关闭/切换字幕。

## 验收
烧录后必须抽帧确认字幕可见，并用 `ffprobe` 确认 H.264/AAC、竖屏尺寸和时长；烧录文件另存为 `videos/burnin/`，不覆盖原视频。
