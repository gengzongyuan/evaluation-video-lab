# LF-10 v2 播放器接入前置门

## 目的

LF-10 讲多步骤 Agent 的调用树。播放器接入前，必须同时通过媒体门、字幕门、内容事实门和证据边界门。本文件不把示意调用树当作当前 Langfuse 实例的真实 Trace。

## 媒体门

- MP4 非空，时长约 180 秒，容差 ±1 秒。
- 画面为 1080×1920，视频 H.264，音频 AAC。
- 使用 `langfuse/scripts/check_video_quality.py` 检查音频非静音。
- 在 0、15、30、60、120、165 秒抽帧，至少三处哈希不同；理想状态为 12 个约 15 秒镜头。
- SRT 与 VTT 均非空、UTF-8 可读，时间码按 15 秒镜头对齐。

## 内容门

画面和旁白必须清楚区分以下节点：

- Agent：规划或编排多个步骤的应用工作单元。
- Retrieval / parse：普通步骤或 Span，用于展示中间处理。
- Tool：外部能力调用，需与模型调用分开讲。
- Generation：模型调用，展示输入、输出、模型和 usage 等字段的语义范围。
- Trace / Observation：外层请求和子节点层级；示意树需展示父子关系。

若展示 JSON 或代码示意，应只使用脱敏占位值，不出现真实 key、secret、Authorization、PII、完整 prompt 或内网地址。

## 真实证据边界

- `type`、`name`、`parentObservationId`、`status` 等字段语义可依据当前官方数据模型核对。
- 示意树能解释排障思路，不能证明当前实例已经创建了 Agent、Tool 或 Generation。
- 当前项目没有安全注入 key，真实 Trace 写入、Worker 消费、UI/API 回读和父子关系核验保持 `BLOCKED`。
- 不得把历史截图、health/readiness、旧 API 迁移提示或空请求认证响应说成当前新 Trace。
- 只有在同一运行保存 Trace ID、脱敏原始响应、当前版本 UI/API 回读和逐字段核对后，才可升级证据等级。

## 接入前检查命令

```bash
python3 langfuse/validate_manifest.py
python3 langfuse/scripts/check_video_quality.py \
  langfuse/videos/LF-10-agent-tree-v2.mp4 \
  --subtitle langfuse/captions/LF-10-v2.srt \
  --subtitle langfuse/captions/LF-10-v2.vtt
rg -n "BLOCKED|prototype / L1|parentObservationId|Generation|Tool" \
  langfuse/lf10-agent-observability-lesson.md \
  langfuse/captions/LF-10-v2.srt
```

没有满足上述检查时，LF-10 保持 `prototype / L1`，不得接入发布目录或表述为真实调用树演示。
