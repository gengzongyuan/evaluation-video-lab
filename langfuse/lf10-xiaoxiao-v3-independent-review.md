# LF-10 Xiaoxiao 原速版独立验收

- 任务：LF10 成片独立音画复核
- 日期：2026-11-23（Asia/Shanghai）
- 审阅：`/root/lf16_otel_audit`
- 对象：`langfuse/videos/LF-10-agent-tree-xiaoxiao-v3.mp4`
- 对照：`langfuse/captions/LF-10-xiaoxiao-v3.srt`、`langfuse/captions/LF-10-xiaoxiao-v3.vtt`、`langfuse/build/lf10-xiaoxiao-v3/timeline.json`、`langfuse/scripts/render_lf10_xiaoxiao_v3.py`
- 声线：`zh-CN-XiaoxiaoNeural`，`rate=-5%`
- 总评：**PASS（媒体合同）**，第 1 镜时长备注
- 成熟度：保持 `prototype / L1`。本文件只证明原速旁白、切镜、烧录字幕和字幕同轴，不证明当前实例已写入 Agent 调用树、同 ID 回读整棵树，或完成真实调度观测。

制作方 QA `langfuse/lf10-xiaoxiao-v3-qa.md` 只作对照，不作为放行依据。下列数字全部由本任务重跑命令和看图得到。

## 结论

这版不是 180 秒拉伸片，也不是单卡冻帧。成片 181.760 秒，20 个唯一构图，单镜 7.488–11.376 秒，底部有烧录中文字幕，SRT/VTT 20 条时间轴和文本完全一致。自然旁白门退出码 0，含 `full_decode` PASS。尾部静音 0.000 秒。

第 1 镜 `hook` 为 11.376 秒，超出 10.000 秒合同 1.376 s。这是时长备注，不是画面锁定失败：20 个中点内容哈希全部不同，字幕同轴。

不能把本 PASS 写成“听起来像真人”、运镜短视频，或“Agent 树已跑通”。质量门不听感，镜内仍是静态 PNG。

## 实测

| 检查 | 结果 | 证据 |
|---|---|---|
| 文件 | 存在 | 4,214,747 bytes |
| 封装时长 | 181.760 s | ffprobe format |
| 视频 | H.264 1080×1920，181.700 s | ffprobe stream 0 |
| 音频 | AAC 24 kHz mono，181.760 s | ffprobe stream 1 |
| 音视频差 | 0.000 s | 自然旁白门 |
| 尾部静音 | 0.000 s | 自然旁白门；`silencedetect=noise=-45dB:d=1.5` 无事件 |
| 响度 | mean -19.6 dB，max -0.5 dB | volumedetect |
| 拉伸 | 未发现 | 自然旁白门 PASS；无尾部静音填充 |
| 镜头 | 20 unique / 20 listed | timeline + 自然旁白门 |
| 构图 | 20 种，相邻不重复 | hook → agent-loop → … → stamp → cta |
| 单镜时长 | 7.488–11.376 s | 第 1 镜 11.376 s 超 10 s |
| 中点画面哈希 | 20/20 不同 | `/tmp/lf10-independent-review/frames` |
| 烧录字幕 | 可见 | 每镜底部黑条中文；与 SRT 短句一致 |
| SRT/VTT | 20/20，时间轴和文本完全相同 | last 00:03:01,800 / 181.800 s；相对视频 gap -0.040 s |
| 乱码 / 敏感值 | 未发现 | 字幕与 timeline 无 U+FFFD、内网地址、Authorization、密钥赋值；input/output/堆栈为遮罩 |
| 自然旁白门 | PASS | 本任务重跑，退出码 0 |

质量门命令：

```bash
python3 langfuse/scripts/check_natural_voice_video.py \
  langfuse/videos/LF-10-agent-tree-xiaoxiao-v3.mp4 \
  --subtitle langfuse/captions/LF-10-xiaoxiao-v3.srt \
  --subtitle langfuse/captions/LF-10-xiaoxiao-v3.vtt \
  --shots langfuse/build/lf10-xiaoxiao-v3/timeline.json
```

输出：

```text
full_decode: PASS
duration: format=181.760s audio=181.760s delta=0.000s
trailing_silence: 0.000s
subtitle LF-10-xiaoxiao-v3.srt: last_end=181.800s gap_to_video=-0.040s
subtitle LF-10-xiaoxiao-v3.vtt: last_end=181.800s gap_to_video=-0.040s
srt_vtt_last_delta: 0.000s
shots: 20 unique / 20 listed
PASS
```

## 画面抽检

已实际查看：

- `/tmp/lf10-independent-review/mids-contact-1.jpg` 01-05
- `/tmp/lf10-independent-review/mids-contact-2.jpg` 06-10
- `/tmp/lf10-independent-review/mids-contact-3.jpg` 11-15
- `/tmp/lf10-independent-review/mids-contact-4.jpg` 16-20

20 个中点都是不同构图。底部烧录字幕清楚，中文无乱码。调用树、Tool args、input/output、错误堆栈都标成示意或已遮罩；第 19 镜明确 `PROTOTYPE / L1`，第 20 镜导向 LF-11。没有真实 Trace ID、密钥或内网地址。

## 时长备注

- 第 1 镜 `hook`：11.376 s（+1.376 s）

其余 19 镜都在 6–10 秒内。序列层面仍有 20 次可感知切镜，但不能把第 1 镜写成满足 10 秒单镜上限。

## 范围外

- 未改播放器、manifest、课程索引或项目权威状态。
- 未 git commit / push。
- 未改配音，未把音频拉伸到 180 秒。
