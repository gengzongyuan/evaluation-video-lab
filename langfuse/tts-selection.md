# 中文旁白试听与选择

日期：2026-11-22

## 本机可复现声音

系统自带 `say` 可用中文声音。当前试听句子位于 `langfuse/tts/`：

- `reed-sample.m4a`：大陆普通话，约 28.5 秒，停连自然度和语速最适合科普旁白，建议作为第一版重制声音。
- `tingting-sample.m4a`：大陆普通话，但同一文本生成约 3 秒，明显不适合当前旁白，暂不采用。

生成命令：

```bash
say -v 'Reed' -r 165 -o reed-sample.aiff -f input.txt
ffmpeg -i reed-sample.aiff -c:a aac -b:a 128k reed-sample.m4a
```

## 字幕方案

重制视频同时输出两份字幕：

1. 视频内烧录字幕，保证用户直接打开 MP4 就能看到；
2. 独立 `.srt` 与 `.vtt`，供播放器切换和后续剪辑。

字幕按 6–10 秒镜头切分，避免一整段旁白只对应一张静态字幕卡。声音、字幕与画面使用同一稿件；没有真实 Langfuse 写入证据的句子继续标记 `prototype / L1`。
