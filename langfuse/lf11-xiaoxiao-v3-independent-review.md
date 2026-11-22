# LF-11 Xiaoxiao 原速版独立验收

- 任务：LF11 成片独立音画复核
- 日期：2026-11-23（Asia/Shanghai）
- 审阅：`/root/lf16_otel_audit`
- 对象：`langfuse/videos/LF-11-compare-xiaoxiao-v3.mp4`
- 对照：`langfuse/captions/LF-11-xiaoxiao-v3.srt`、`langfuse/captions/LF-11-xiaoxiao-v3.vtt`、`langfuse/build/lf11-xiaoxiao-v3/timeline.json`、`langfuse/scripts/render_lf11_xiaoxiao_v3.py`
- 声线：`zh-CN-XiaoxiaoNeural`，`rate=-5%`
- 总评：**PASS（媒体合同）**，第 14 镜时长备注
- 成熟度：保持 `prototype / L1`。本文件只证明原速旁白、切镜、烧录字幕和字幕同轴，不证明当前实例已完成 Dataset 对照实验、run A/B 回读或统计显著。

制作方 QA 若存在只作对照，不作为放行依据。下列数字全部由本任务重跑命令和看图得到。

## 结论

这版不是 180 秒拉伸片，也不是单卡冻帧。成片 170.900 秒，20 个唯一构图，单镜 7.320–10.032 秒，底部有烧录中文字幕，SRT/VTT 20 条时间轴和文本完全一致。自然旁白门退出码 0，含 `full_decode` PASS。尾部静音 0.000 秒。

第 14 镜 `cost-latency` 为 10.032 秒，超出 10.000 秒合同 32ms。这是时长备注，不是画面锁定失败：20 个中点内容哈希全部不同，字幕同轴。

不能把本 PASS 写成“听起来像真人”、运镜短视频，或“对照实验已完成”。质量门不听感，镜内仍是静态 PNG。

## 实测

| 检查 | 结果 | 证据 |
|---|---|---|
| 文件 | 存在 | 3,679,037 bytes |
| 封装时长 | 170.900 s | ffprobe format |
| 视频 | H.264 1080×1920，170.867 s | ffprobe stream 0 |
| 音频 | AAC 24 kHz mono，170.884 s | ffprobe stream 1 |
| 音视频差 | 0.016 s | 自然旁白门 |
| 尾部静音 | 0.000 s | 自然旁白门；`silencedetect=noise=-45dB:d=1.5` 无事件 |
| 响度 | mean -19.6 dB，max -1.6 dB | volumedetect |
| 拉伸 | 未发现 | 自然旁白门 PASS；无尾部静音填充 |
| 镜头 | 20 unique / 20 listed | timeline + 自然旁白门 |
| 构图 | 20 种，相邻不重复 | hook → shared-dataset → … → stamp → cta |
| 单镜时长 | 7.320–10.032 s | 第 14 镜 10.032 s 略超 10 s |
| 中点画面哈希 | 20/20 不同 | `/tmp/lf11-independent-review/frames` |
| 烧录字幕 | 可见 | 每镜底部黑条中文；与 SRT 短句一致 |
| SRT/VTT | 20/20，时间轴和文本完全相同 | last 00:02:50,904 / 170.904 s；相对视频 gap -0.004 s |
| 乱码 / 敏感值 | 未发现 | 字幕与 timeline 无 U+FFFD、内网地址、Authorization、密钥赋值；对照值为示意 |
| 自然旁白门 | PASS | 本任务重跑，退出码 0 |

质量门命令：

```bash
python3 langfuse/scripts/check_natural_voice_video.py \
  langfuse/videos/LF-11-compare-xiaoxiao-v3.mp4 \
  --subtitle langfuse/captions/LF-11-xiaoxiao-v3.srt \
  --subtitle langfuse/captions/LF-11-xiaoxiao-v3.vtt \
  --shots langfuse/build/lf11-xiaoxiao-v3/timeline.json
```

输出：

```text
full_decode: PASS
duration: format=170.900s audio=170.884s delta=0.016s
trailing_silence: 0.000s
subtitle LF-11-xiaoxiao-v3.srt: last_end=170.904s gap_to_video=-0.004s
subtitle LF-11-xiaoxiao-v3.vtt: last_end=170.904s gap_to_video=-0.004s
srt_vtt_last_delta: 0.000s
shots: 20 unique / 20 listed
PASS
```

## 画面抽检

已实际查看：

- `/tmp/lf11-independent-review/mids-contact-1.jpg` 01-05
- `/tmp/lf11-independent-review/mids-contact-2.jpg` 06-10
- `/tmp/lf11-independent-review/mids-contact-3.jpg` 11-15
- `/tmp/lf11-independent-review/mids-contact-4.jpg` 16-20

20 个中点都是不同构图。底部烧录字幕清楚，中文无乱码。平均分、item、run A/B、对照表都标成示意；第 19 镜明确 `PROTOTYPE / L1`，第 20 镜导向 LF-12。没有真实 Dataset run ID、密钥或内网地址。

## 时长备注

- 第 14 镜 `cost-latency`：10.032 s（+32 ms）

其余 19 镜都在 6–10 秒内。序列层面每 6–10 秒可感知变化成立。

## 范围外

- 未改播放器、manifest、课程索引或项目权威状态。
- 未 git commit / push。
- 未改配音，未把音频拉伸到 180 秒。
