# LF-01 Xiaoxiao 原速版验收

日期：2026-11-22（Asia/Shanghai）

## 文件

- 视频：`langfuse/videos/LF-01-langfuse-overview-xiaoxiao-v3.mp4`
- 字幕：`langfuse/captions/LF-01-xiaoxiao-v3.srt`、`.vtt`
- 声线：`zh-CN-XiaoxiaoNeural`，`rate=-5%`
- 状态：`prototype / L1`

## 实测

- 时长 173.033 秒（2026-11-23 重渲第 4 镜乱码配音后），不是把短旁白拉伸到 180 秒。
- 视频 1080×1920，H.264；音频 AAC。
- 音视频时长差约 0.03 秒。
- `volumedetect`：mean -19.8 dB，max -3.3 dB；尾部无 1.2 秒以上静音。
- 24 个镜头，构图轮换：钩子、对照、流程、Observation/Span、调用树、health ≠ Trace、证据闭环、CTA。第 4 镜口播为「最后那句答案」；第 6 镜改为 Trace 下先挂 Observation。
- 每镜底部烧录字幕；SRT/VTT 同一时间轴，最后一条 00:02:41.280 → 00:02:53.088。
- 字幕覆盖到片尾，无 `U+FFFD`，无内网地址/密钥。

## 明确 FAIL 的旧片

`LF-01-langfuse-overview-xiaoxiao.mp4` 把 129.576 秒原速音频拉到约 180 秒，画面仍是 12 张 15 秒卡片，不得再作为推荐播放文件。

## 仍不能证明

当前实例 Trace 写入、Worker 消费、回读、真实 UI。本片只证明制作流程：原速 Xiaoxiao、画面内字幕、镜头切换。
