# LF-10 Xiaoxiao 原速版验收

日期：2026-11-23（Asia/Shanghai）

## 文件

- 视频：`langfuse/videos/LF-10-agent-tree-xiaoxiao-v3.mp4`
- 字幕：`langfuse/captions/LF-10-xiaoxiao-v3.srt`、`langfuse/captions/LF-10-xiaoxiao-v3.vtt`
- 渲染器：`langfuse/scripts/render_lf10_xiaoxiao_v3.py`
- 分镜来源：`langfuse/LF-10-shot-board-xiaoxiao.md`
- 声线：`zh-CN-XiaoxiaoNeural`，`rate=-5%`
- 状态：`prototype / L1`

## 实测

- 成片 181.760 秒（3 分 02 秒）；20 段独立原速配音，无音频拉伸、无尾部静音填充。时长由旁白决定，略超 180 秒。
- 视频 1080×1920，H.264；音频 AAC。
- 音视频时长差 0.000 秒，尾部静音 0.000 秒。
- 20 个唯一镜头 ID、20 种构图；单镜约 7.488–11.376 秒。第 1 镜 11.376 秒略超 10 秒，保持原速，不视为拉伸缺陷。
- 主 agent 按 20 个镜头中点抽帧：构图全部不同，底部烧录中文字幕可见，无乱码、无密钥或内网地址。
- SRT/VTT 各 20 条，时间轴一致，最后一条均为 181.800 秒。
- 自然旁白质量门退出码 0，结果 `PASS`（含 full_decode）。
- Agent 树、Tool、Generation、耗时和 Trace ID 均为示意。

质量门命令：

```bash
python3 langfuse/scripts/check_natural_voice_video.py \
  langfuse/videos/LF-10-agent-tree-xiaoxiao-v3.mp4 \
  --subtitle langfuse/captions/LF-10-xiaoxiao-v3.srt \
  --subtitle langfuse/captions/LF-10-xiaoxiao-v3.vtt \
  --shots langfuse/build/lf10-xiaoxiao-v3/timeline.json
```

## 证据边界

本片只解释多步骤 Agent 调用树、节点类型和回读口径。不证明当前实例已写入 Agent Trace、完成树回读，或验证工具调用安全。
