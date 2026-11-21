# Langfuse v2 快切样片生产规范

核对日期：2026-11-22（Asia/Shanghai）

## 目的

v2 样片用于验证“3 分钟科普短视频”是否真正可观看。它不能只满足 MP4 有音视频流，还必须让观众在手机竖屏上持续获得新的信息、画面和旁白。

## 镜头节奏

- 单集目标时长约 180 秒。
- 至少 12 个镜头，默认每镜约 15 秒；连续讲解中可使用 3–8 秒的切点或局部动画。
- 每个镜头至少发生一种可见变化：标题、调用树层级、代码行、证据卡、箭头、状态标签或关键数字。
- 0–3 秒给出问题钩子；中段展示概念或最小流程；结尾给一句话结论、证据边界和下一集 CTA。
- 禁止把一张静态卡片循环 180 秒，也禁止用“有 AAC 音轨”替代可听旁白���

## 旁白与字幕

- 使用真实中文旁白；生成方式和声音版本写入 QA 文件。
- 音频必须经过 `ffmpeg -af volumedetect` 检查，`mean_volume` 和 `max_volume` 都不能是 `-inf`。
- 字幕按镜头或句子切分，SRT 与 VTT 时间轴覆盖完整视频；字幕文字不能超出证据等级。
- 旁白、画面和字幕必须使用同一知识点和同一状态口径。

## 画面与证据

- 画面可以是信息图、代码示意、脱敏 UI 或真实录屏；若没有真实运行证据，必须显式标注 `prototype / L1`。
- health、readiness、认证门或历史截图不能被包装成新 Trace、Dataset run、Score 写入或回读成功。
- 真实 UI/API 录屏需要版本、时间、脱敏 payload、Trace/Run/Score ID 和回读证据；未满足前保持 prototype。

## v2 验收命令

```bash
python3 langfuse/validate_manifest.py
ffprobe -v error -show_entries format=duration:stream=codec_type,codec_name,width,height -of json <video.mp4>
ffmpeg -i <video.mp4> -af volumedetect -f null -
for t in 0 15 30 60 120 165; do
  ffmpeg -y -ss "$t" -i <video.mp4> -frames:v 1 -update 1 "/tmp/frame-$t.png"
done
```

## LF-01 v2 对照结果

- 文件：`videos/LF-01-langfuse-overview-v2.mp4`
- QA：`lf01-v2-qa.md`
- 12 个 15 秒镜头，已抽查 0、15、30、60、120、165 秒。
- 180 秒、1080×1920、H.264/AAC；音量 mean `-26.0 dB`、max `-1.7 dB`。
- 状态仍为 `prototype / L1`；该样片证明的是音画制作流程，不是 Langfuse 实例写入或回读。

## 扩展规则

只有 LF-01 v2 通过人工听看和上述命令后，才按同一规范制作 LF-02 及后续集数。任何一项失败都要回退为 `blocked`，不得仅凭文件存在或编码成功放行。
