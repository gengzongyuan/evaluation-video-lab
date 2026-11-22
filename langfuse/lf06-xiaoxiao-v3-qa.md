# LF-06 Xiaoxiao 原速版验收

日期：2026-11-23（Asia/Shanghai）

## 文件

- 视频：`langfuse/videos/LF-06-score-xiaoxiao-v3.mp4`
- 字幕：`langfuse/captions/LF-06-xiaoxiao-v3.srt`、`langfuse/captions/LF-06-xiaoxiao-v3.vtt`
- 渲染器：`langfuse/scripts/render_lf06_xiaoxiao_v3.py`
- 分镜来源：`langfuse/LF-06-shot-board-xiaoxiao.md`
- 声线：`zh-CN-XiaoxiaoNeural`，`rate=-5%`
- 状态：`prototype / L1`

## 实测

- 成片 171.266 秒（2 分 51 秒）；20 段独立原速配音，无音频拉伸、无尾部静音填充。
- 20 段渲染口播与 LF-06 Xiaoxiao 分镜板逐字一致，没有改词。
- 视频 1080×1920，H.264；音频 AAC。
- 音视频时长差 0.034 秒，尾部静音 0.000 秒。
- `volumedetect`：mean -19.6 dB，max -2.5 dB。
- 20 个唯一镜头 ID、20 种构图；单镜约 7.488–10.176 秒。抽帧检查 0s、85s、155s，底部字幕清楚可见。
- 每镜底部烧录字幕；SRT/VTT 各 20 条，时间轴一致，最后一条均为 171.312 秒。
- 首次合成文件可被 ffprobe 读到时长，但整段解码报 Invalid NAL / AAC 错误。已重合成，`ffmpeg -v error -xerror` 整段解码通过。
- 自然旁白质量门退出码 0，结果 `PASS`（含新增 full_decode 检查）。
- Score、90 分、失败样本和关联对象均为示意。
- 视频、字幕、渲染器和本 QA 未发现 `U+FFFD`、内网地址或密钥字样。

质量门命令：

```bash
python3 langfuse/scripts/check_natural_voice_video.py \
  langfuse/videos/LF-06-score-xiaoxiao-v3.mp4 \
  --subtitle langfuse/captions/LF-06-xiaoxiao-v3.srt \
  --subtitle langfuse/captions/LF-06-xiaoxiao-v3.vtt \
  --shots langfuse/build/lf06-xiaoxiao-v3/timeline.json
```

## 证据边界

本片只解释 Evaluation、Score、评分方法、失败抽查和发布闸门的概念口径。不证明当前实例已写入 Score、完成 Dataset run、同 ID 回读或通过上线决策。
