# LF-04 v2 播放器接入前检查

## 目标

LF-04 主题为 Prompt 管理、版本和 label。当前播放器中的 LF-04 仍是旧版原型；只有新的快切资产通过以下门禁后，才能替换链接。

## 必须存在的资产

- `langfuse/videos/LF-04-prompt-management-v2.mp4`
- `langfuse/captions/LF-04-v2.srt`
- `langfuse/captions/LF-04-v2.vtt`
- `langfuse/lf04-v2-qa.md`

## 媒体门

```bash
python3 langfuse/scripts/check_video_quality.py \
  langfuse/videos/LF-04-prompt-management-v2.mp4 \
  --subtitle langfuse/captions/LF-04-v2.srt \
  --subtitle langfuse/captions/LF-04-v2.vtt
```

必须通过：约 180 秒、1080×1920、H.264/AAC、音频非静音、0/15/30/60/120/165 秒抽帧存在至少 3 个不同画面、字幕文件非空。

## 内容与证据门

- 至少 12 个约 15 秒镜头，画面随 Prompt 文本、版本号、label、Trace metadata 或决策卡变化。
- 中文旁白必须与字幕逐镜对应，不能只生成占位音频。
- 课程可以讲 Prompt 版本和 label 的概念与官方字段语义。
- 没有受保护项目 key、当前 SDK 版本、版本回读和 Trace ID 前，不得声称当前实例已成功创建或读取 Prompt。
- `prototype / L1` 必须出现在画面或 QA 记录中；不能把示意 UI 说成真实 UI 录屏。

## 接入动作

1. 确认上述四个文件非空。
2. 运行媒体质量门并保存输出。
3. 人工抽查至少 0、15、60、120、165 秒画面和对应字幕。
4. 通过后才把播放器 LF-04 链接切换到 v2，并在 `series-index.md` 标为 `prototype / L1`。
5. 若任何证据缺失，保留旧版链接并记录 `blocked`，不升级 manifest 证据等级。

当前状态：`preflight / waiting for LF-04 v2 assets`。
