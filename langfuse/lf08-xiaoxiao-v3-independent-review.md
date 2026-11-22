# LF-08 Xiaoxiao 原速版独立验收

- 任务：LF08 成片独立音画复核
- 日期：2026-11-23（Asia/Shanghai）
- 审阅：`/root/lf16_otel_audit`
- 对象：`langfuse/videos/LF-08-feedback-xiaoxiao-v3.mp4`
- 对照：`langfuse/captions/LF-08-xiaoxiao-v3.srt`、`langfuse/captions/LF-08-xiaoxiao-v3.vtt`、`langfuse/build/lf08-xiaoxiao-v3/timeline.json`、`langfuse/scripts/render_lf08_xiaoxiao_v3.py`
- 声线：`zh-CN-XiaoxiaoNeural`，`rate=-5%`
- 总评：**PASS（媒体合同）**
- 成熟度：保持 `prototype / L1`。本文件只证明原速旁白、切镜、烧录字幕和字幕同轴，不证明当前实例已收到用户反馈、写入 Score、同 ID 回读或完成反馈回流。

制作方 QA `langfuse/lf08-xiaoxiao-v3-qa.md` 只作对照，不作为放行依据。下列数字全部由本任务重跑命令和看图得到。

## 结论

这版不是 180 秒拉伸片，也不是单卡冻帧。成片 173.166 秒，20 个唯一构图，单镜 7.560–9.744 秒，全部落在 6–10 秒合同内。底部有烧录中文字幕，SRT/VTT 20 条时间轴和文本完全一致。自然旁白门退出码 0，含 `full_decode` PASS。尾部静音 0.000 秒。

不能把本 PASS 写成“听起来像真人”、运镜短视频，或“反馈已回流 / Score 已验证”。质量门不听感，镜内仍是静态 PNG。

## 实测

| 检查 | 结果 | 证据 |
|---|---|---|
| 文件 | 存在 | 3,922,035 bytes |
| 封装时长 | 173.166 s | ffprobe format |
| 视频 | H.264 1080×1920，173.133 s | ffprobe stream 0 |
| 音频 | AAC 24 kHz mono，173.125 s | ffprobe stream 1 |
| 音视频差 | 0.041 s | 自然旁白门 |
| 尾部静音 | 0.000 s | 自然旁白门；`silencedetect=noise=-45dB:d=1.5` 无事件 |
| 响度 | mean -19.6 dB，max -1.0 dB | volumedetect |
| 拉伸 | 未发现 | 自然旁白门 PASS；无尾部静音填充 |
| 镜头 | 20 unique / 20 listed | timeline + 自然旁白门 |
| 构图 | 20 种，相邻不重复 | hook → single-event → … → stamp → cta |
| 单镜时长 | 7.560–9.744 s | 全部落在 6–10 秒合同内 |
| 中点画面哈希 | 20/20 不同 | `/tmp/lf08-independent-review/frames` |
| 烧录字幕 | 可见 | 每镜底部黑条中文；与 SRT 短句一致 |
| SRT/VTT | 20/20，时间轴和文本完全相同 | first 00:00:00,000；last 00:02:53,232 / 173.232 s；相对视频 gap -0.066 s |
| 乱码 / 敏感值 | 未发现 | 字幕与 timeline 无 U+FFFD、内网地址、Authorization、密钥赋值；ID 使用占位符 |
| 自然旁白门 | PASS | 本任务重跑，退出码 0 |

质量门命令：

```bash
python3 langfuse/scripts/check_natural_voice_video.py \
  langfuse/videos/LF-08-feedback-xiaoxiao-v3.mp4 \
  --subtitle langfuse/captions/LF-08-xiaoxiao-v3.srt \
  --subtitle langfuse/captions/LF-08-xiaoxiao-v3.vtt \
  --shots langfuse/build/lf08-xiaoxiao-v3/timeline.json
```

输出：

```text
full_decode: PASS
duration: format=173.166s audio=173.125s delta=0.041s
trailing_silence: 0.000s
subtitle LF-08-xiaoxiao-v3.srt: last_end=173.232s gap_to_video=-0.066s
subtitle LF-08-xiaoxiao-v3.vtt: last_end=173.232s gap_to_video=-0.066s
srt_vtt_last_delta: 0.000s
shots: 20 unique / 20 listed
PASS
```

## 画面抽检

已实际查看：

- `/tmp/lf08-independent-review/mids-contact-1.jpg` 01-05
- `/tmp/lf08-independent-review/mids-contact-2.jpg` 06-10
- `/tmp/lf08-independent-review/mids-contact-3.jpg` 11-15
- `/tmp/lf08-independent-review/mids-contact-4.jpg` 16-20

20 个中点都是不同构图。底部烧录字幕清楚，中文无乱码。点踩、满意度、Trace ID、评论原文都标成示意或已脱敏；第 19 镜明确 `PROTOTYPE / L1`，第 20 镜导向 LF-09。没有真实用户原文、密钥或内网地址。

## 范围外

- 未改播放器、manifest、课程索引或项目权威状态。
- 未 git commit / push。
- 未改配音，未把音频拉伸到 180 秒。
