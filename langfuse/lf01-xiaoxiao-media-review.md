# LF-01 Xiaoxiao 媒体与音频独立复核

- 任务：LF01-A1
- 日期：2026-11-22
- 输入：`langfuse/videos/LF-01-langfuse-overview-xiaoxiao.mp4`、`langfuse/captions/LF-01-xiaoxiao.srt`、`langfuse/captions/LF-01-xiaoxiao.vtt`、`langfuse/tts/neural/LF-01-xiaoxiao-full.m4a`、`langfuse/tts/neural/LF-01-xiaoxiao-full.mp3`、`langfuse/LF-01-voice-script-v2.md`
- 总评：**FAIL**
- 成熟度口径：保��� `prototype / L1`。本文件只证明媒体/字幕/节奏检查，不证明 Langfuse 实例写入、回读或生产可用性。

## 结论

这版 LF-01 通过了现有弱媒体门（时长、1080×1920、H.264/AAC、非静音、6 个抽帧点画面哈希不同、SRT/VTT 文件非空），但**不能作为用户要求的“有人味 Xiaoxiao + 可看字幕”成品**。

阻断项：

1. **旁白被整体拉慢约 1.39 倍。** 原始 Xiaoxiao 整段 MP3 是 129.576 秒；视频音轨和 `LF-01-xiaoxiao-full.m4a` 都是 179.934 秒。VTT 停在 129.486 秒，SRT 被拉到 179.842 秒。这不是自然停连，是把神经 TTS 用时间拉伸填满 180 秒，听感会发黏、发空。
2. **SRT 与 VTT 时间轴不一致。** 26 条文本相同，但 VTT 按原速、SRT 按慢速。播放器若加载 VTT，字幕会在约 2:09 结束，后面空 50 秒。
3. **画面仍是 15 秒卡片，不是 6–10 秒快切。** `select=gt(scene\,0.08)` 只打出 6 个切点：15 / 30 / 60 / 105 / 120 / 150 秒。严格门禁要求至少 18 次预筛变化。
4. **视频内没有烧录字幕。** 外挂字幕存在，但当前 ffmpeg 无 `subtitles/ass/drawtext`，直接打开 MP4 看不到字幕。

机器门 `python3 langfuse/scripts/check_video_quality.py ...` 返回 PASS，不能覆盖上述问题。

## 我的理解

用户已经选定 Xiaoxiao Neural，并要求加字幕。验收必须分开三层：

- 编码层：有没有可播放的音视频；
- 旁白层：是不是 Xiaoxiao，以及有没有被拉速、有没有长静音；
- 观看层：字幕是否同步、是否烧进画面、镜头是否真的在变。

本任务只做 A1 媒体/音频复核，不改视频、字幕、manifest、播放器或项目状态。

## 隐含假设

- `LF-01-xiaoxiao-full.mp3` 是未拉伸的原始 edge-tts 输出；`m4a` 与 MP4 音轨是同一条被对齐到 180 秒的音频。
- 时间比 179.842 / 129.486 ≈ 1.3889，等价于 `atempo≈0.72`。未反解具体滤镜，但时长差足以定性。
- 我无法在本环境做真人听感评分；“有人味”只能用声线来源、语速、响度动态和静音结构间接判断。用户已认可的是 **129 秒原速 Xiaoxiao 试听**，不是这条被拉到 180 秒的音轨。

## 能证明的范围

| 项 | 结果 | 证据 |
|---|---|---|
| 视频存在 | PASS | 3.6M，`duration=180.046` |
| 编码 | PASS | H.264 1080×1920 + AAC 24 kHz mono，约 99.5 kbps |
| 非静音 | PASS | `mean_volume -19.5 dB`，`max_volume -3.0 dB`；loudnorm Input Integrated -19.3 LUFS，True Peak -2.8 dBTP |
| 无超 1 秒死静音 | PASS | 30 段静音，最长 0.976s，合计 26.474s，全部是句间空隙 |
| 口播文本覆盖 20 段脚本 | PASS | SRT 26 cue 去标点后与 `LF-01-voice-script-v2.md` 20 行拼接一致；仅去掉原稿引号 |
| 事实边界句仍在 | PASS | cue 25 保留 `prototype / L1`；cue 18 保留 health 200 不等于新 Trace |
| 现有质量脚本 | PASS | `check_video_quality.py` PASS；`qa_fastcut_video.py` PASS |
| 原速 Xiaoxiao 资产仍在 | PASS | `LF-01-xiaoxiao-full.mp3` 129.576s，音量与成片接近 |

## 不能证明的范围

- 不能证明“听起来像真人”。LRA 只有 2.9 LU，动态很平，符合 TTS，不是口播。
- 不能证明成片声线就是试听通过的 Xiaoxiao 自然语速；成片被拉到约 3.52 字/秒，原速 VTT 约 4.89 字/秒。
- 不能证明字幕已烧进画面。
- 不能证明 6 个抽帧点变化等于 20 个可感知镜头。场景预筛只有 6 次。
- 不能证明 Langfuse 真实运行。内容仍是示意。

## 与其他 agent 的冲突

- 制作侧把“对齐 180 秒视频”做成了整段 `atempo`，和用户选定的 Xiaoxiao 自然试听冲突。
- `check_video_quality.py` 只抽 0/15/30/60/120/165，6/6 unique 就会 PASS，和严格快切门禁冲突。
- SRT 与 VTT 不应同时登记为“已对齐字幕”。当前只有 SRT 对得上慢速成片；VTT 对得上原速 MP3。
- 画面节奏的最终判定归 LF01-A2。A1 只记录场景预筛失败，不替代抽帧审片。

## 需要冻结的字段

- 声线：`zh-CN-XiaoxiaoNeural`，`rate=-5%`，**禁止再整段拉伸到 180 秒**。
- 成片时长策略：口播多长，视频就多长；或按镜头重切画面去贴原速音频，而不是把人声拉成 3 分钟。
- 字幕：SRT 与 VTT 必须同一时间轴，误差 < 50ms；禁止 15 分钟时间码和乱码。
- 状态：`prototype / L1`。
- 旧媒体门不能单独放行。

## 依据

命令与结果（工作目录 `evaluation-video-lab`）：

```text
ffprobe 视频 duration=180.046；video=h264 1080x1920；audio=aac 24000Hz mono 99502bps duration=179.934
ffprobe 原始 mp3 duration=129.576
ffmpeg volumedetect：mean -19.5 dB / max -3.0 dB
ffmpeg loudnorm：Input Integrated -19.3 LUFS，True Peak -2.8 dBTP，LRA 2.9 LU
silencedetect noise=-40dB:d=0.5：30 events，max 0.976s，sum 26.474s，none > 1.0s
select=gt(scene,0.08)：6 pts  15.046, 30.046, 60.046, 105.046, 120.046, 150.046
python3 langfuse/scripts/check_video_quality.py ... PASS
python3 langfuse/scripts/qa_fastcut_video.py ... PASS
```

字幕统计：

| 文件 | cue 数 | 起止 | 覆盖 |
|---|---:|---|---|
| SRT | 26 | 0.139–179.842 | 对齐慢速成片，片尾余 0.204s |
| VTT | 26 | 0.100–129.486 | 对齐原速 MP3，相对成片空 50.56s |

其他字幕问题：cue 1/2 重叠 70ms；最长 cue 12.225s（边界说明句）；无 `15:00`、乱码、内网地址或密钥。

## 产物

仅本文件：`langfuse/lf01-xiaoxiao-media-review.md`。

## 验证

- 媒体弱门：PASS
- 原速旁白：FAIL（被拉到 180s）
- 字幕一致性：FAIL（SRT≠VTT 时间轴）
- 烧录字幕：FAIL（未嵌入）
- 严格快切预筛：FAIL（6 < 18）
- 证据夸大：未发现把示意写成已验证运行

## 风险 / 缺口

- 若只把 Xiaoxiao 成片推给用户，会再次出现“音频像被拖慢、画面还是卡片、点开没有字幕”。
- 现有质量脚本会继续放行这类片。
- 我没有逐秒听完整 180 秒；听感判断依赖时长比和响度动态，不是听力评分。

## 未完成

- 未重导出原速音画对齐版本。
- 未烧录字幕。
- 未修复 VTT。
- 未做 A2 的逐 8 秒人工抽帧（本任务不写画面审片结论）。

## 建议下一步

1. 用 `LF-01-xiaoxiao-full.mp3`（129.576s）做主音轨，**不要**再 stretch。
2. 画面按 VTT 原速切 26 镜，总时长跟旁白走；若必须 180 秒，就加内容，不要拉人声。
3. 从同一时间轴同时写 SRT 和 VTT，消除 70ms 重叠。
4. 补烧录字幕版 `LF-01-langfuse-overview-xiaoxiao-captioned.mp4`。
5. 在质量门增加：原音频时长与成片音轨差 < 1s、SRT/VTT 结束时间差 < 0.05s、scene 预筛 ≥ 18。

交接格式完。
