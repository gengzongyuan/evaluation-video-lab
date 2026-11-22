# LF-12 Xiaoxiao 原速版验收

日期：2026-11-23（Asia/Shanghai）

## 文件

- 视频：`langfuse/videos/LF-12-incident-xiaoxiao-v3.mp4`
- 字幕：`langfuse/captions/LF-12-xiaoxiao-v3.srt`、`langfuse/captions/LF-12-xiaoxiao-v3.vtt`
- 渲染器：`langfuse/scripts/render_lf12_xiaoxiao_v3.py`
- 分镜来源：`langfuse/LF-12-shot-board-xiaoxiao.md`
- 声线：`zh-CN-XiaoxiaoNeural`，`rate=-5%`
- 状态：`prototype / L1`

## 实测

- 成片 173.633 秒（2 分 54 秒）；20 段独立原速配音，无音频拉伸、无尾部静音填充。
- 20 段渲染口播与 LF-12 Xiaoxiao 分镜板逐字一致，没有改词。
- 视频 1080×1920，H.264；音频 AAC。
- 音视频时长差 0.034 秒，尾部静音 0.000 秒。
- `volumedetect`：mean -19.6 dB，max -1.7 dB。
- 20 个唯一镜头 ID、20 种构图；单镜约 7.296–10.008 秒。抽帧检查 20 个镜头中点，底部字幕清楚可见。
- 每镜底部烧录字幕；SRT/VTT 各 20 条，时间轴一致，最后一条均为 173.688 秒。
- 自然旁白质量门退出码 0，结果 `PASS`（含 full_decode）。
- 第 2 镜 10.008 秒略超 10 秒，保持原速，未拉伸。
- 异常曲线、commit、回归分数、告警阈值均为示意或留空。
- 视频、字幕、渲染器和本 QA 未发现 `U+FFFD`、内网地址或密钥字样。

质量门命令：

```bash
python3 langfuse/scripts/check_natural_voice_video.py \
  langfuse/videos/LF-12-incident-xiaoxiao-v3.mp4 \
  --subtitle langfuse/captions/LF-12-xiaoxiao-v3.srt \
  --subtitle langfuse/captions/LF-12-xiaoxiao-v3.vtt \
  --shots langfuse/build/lf12-xiaoxiao-v3/timeline.json
```

## 证据边界

本片只解释异常信号 → Trace 定位 → 修复 commit → 固定回归集 → 回读与回滚门槛的方法口径。不证明当前实例已定位真实异常 Trace、已提交修复，或回归已经通过。

## 主 agent 抽帧

按 20 个镜头中点抽帧：构图全部不同，底部烧录字幕可见。Dashboard、commit、before/after 和告警数值均为示意。
