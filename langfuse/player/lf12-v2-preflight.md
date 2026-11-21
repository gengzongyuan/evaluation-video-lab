# LF-12 v2 播放器接入前置门

## 媒体门

- MP4 约 180 秒，1080×1920，H.264 视频和 AAC 音频。
- 音频 `volumedetect` 的 mean/max 不得为 `-inf`。
- 在 0、15、30、60、120、165 秒抽帧，至少有 3 个不同画面；目标是 12 个约 15 秒镜头。
- SRT/VTT 非空、UTF-8、时间码按 15 秒镜头递进，且与旁白逐镜对应。

## 内容与证据门

画面和字幕可以讲调试方法，但必须把以下对象分开：

1. **异常信号**：错误率、延迟、成本或用户反馈触发的线索，不等于根因。
2. **Trace 定位**：时间、版本、session 或 request ID 只能定位候选运行；必须保存本轮 Trace ID 和原始回读。
3. **根因分类**：模型、工具、数据、权限、配置和环境的分类是调查框架，不是自动诊断结果。
4. **修复 commit**：保存代码版本、配置差异和变更原因，不能用口头“已修复”替代。
5. **回归 run**：用固定 Dataset/回归样本重跑，保存修复前后逐 item 结果、失败类型、Score、运行参数和版本。
6. **告警与回滚**：阈值、观察窗口和回滚动作必须有记录；Dashboard 截图不能替代闭环证据。

## 阻断边界

当前没有受保护项目 key、同一 Trace 的原始回读和修复后回归 run 时：

- 真实 Trace 定位、修复前后对照、回归通过、告警闭环和回滚安全均保持 `BLOCKED` 或 `needs-review`。
- 不得把示意异常、历史截图、健康检查或单次 Dashboard 当作当前修复成功证明。
- 不得把“错误率下降”或“回归通过”写成事实，除非同一数据、版本、运行条件和原始结果齐全。
- 视频继续标记 `prototype / L1`，不升级为真实生产排障演示。

## 接入前命令

```bash
python3 langfuse/scripts/check_video_quality.py \
  langfuse/videos/LF-12-debug-regression-v2.mp4 \
  --subtitle langfuse/captions/LF-12-v2.srt \
  --subtitle langfuse/captions/LF-12-v2.vtt
python3 langfuse/validate_manifest.py
```

只有媒体质量门、字幕逐字/时间码检查和上述证据边界同时通过，才允许把 LF-12 v2 链接加入播放器和课程索引；本文件本身不改变 manifest 的 episode 状态。
