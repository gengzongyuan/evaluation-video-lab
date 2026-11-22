# LF-05 Xiaoxiao 原速版独立验收

- 任务：LF05 成片独立音画复核
- 日期：2026-11-23（Asia/Shanghai）
- 对象：`langfuse/videos/LF-05-dataset-xiaoxiao-v3.mp4`
- 对照：`langfuse/captions/LF-05-xiaoxiao-v3.srt`、`langfuse/captions/LF-05-xiaoxiao-v3.vtt`、`langfuse/build/lf05-xiaoxiao-v3/timeline.json`、`langfuse/scripts/render_lf05_xiaoxiao_v3.py`
- 总评：**PASS（媒体合同）**
- 成熟度：保持 `prototype / L1`。本文件只证明原速旁白、切镜、烧录字幕和字幕同轴，不证明当前实例已创建 Dataset、完成 run、写入 Score 或回读实验。

制作方 QA `langfuse/lf05-xiaoxiao-v3-qa.md` 只作对照，不作为放行依据。下列数字全部由本任务重跑命令和看图得到。

## 结论

这版不是 180 秒拉伸片，也不是 12 张 15 秒静卡。成片 173.071 秒，20 个唯一构图，单镜 7.128–9.936 秒，底部有烧录中文字幕，SRT/VTT 20 条时间轴和文本完全一致。自然旁白门退出码 0。

8 秒等间隔抽帧会在同一镜内落到两张相同画面（0s/8s 都是 01/20，128s/136s 都是 16/20，168s/172s 都是 20/20），因为这些镜头本身约 9.7–9.8 秒，不是跨镜冻帧。20 个镜头中点画面哈希全部不同。

不能把本 PASS 写成“听起来像真人”或“Dataset 实验已跑通”。`intro-demo-v1`、`item_demo_01` 都是示意。

## 实测

| 检查 | 结果 | 证据 |
|---|---|---|
| 文件 | 存在 | 3,839,683 bytes |
| 封装时长 | 173.071 s | ffprobe format |
| 视频 | H.264 1080×1920 30 fps，173.000 s | ffprobe stream 0 |
| 音频 | AAC 24 kHz mono，173.071 s | ffprobe stream 1 |
| 音视频差 | 0.000 s（format vs audio） | 视频流短 0.071 s，仍 < 0.35 s |
| 尾部静音 | 0.000 s | 自然旁白门；`silencedetect=noise=-45dB:d=1.5` 无事件 |
| 响度 | mean -19.6 dB，max -2.2 dB | volumedetect |
| 镜头 | 20 unique / 20 listed | timeline + 自然旁白门 |
| 构图 | 20 种，相邻不重复 | hook → two-demo → dataset-card → … → cta |
| 单镜时长 | 7.128–9.936 s | 全部落在 6–10 秒合同内 |
| 中点画面哈希 | 20/20 不同 | 独立计算 |
| 烧录字幕 | 可见 | 每镜底部黑条中文；与 SRT 短句一致 |
| SRT/VTT | 20/20，时间轴和文本完全相同 | first 0.000，last 173.112；相对视频 gap -0.041 s |
| 乱码 / 敏感值 | 未发现 | 字幕、渲染器、分镜板无 U+FFFD、内网地址、Authorization、密钥赋值 |
| 自然旁白门 | PASS | 本任务重跑，退出码 0 |

质量门命令：

```bash
python3 langfuse/scripts/check_natural_voice_video.py \
  langfuse/videos/LF-05-dataset-xiaoxiao-v3.mp4 \
  --subtitle langfuse/captions/LF-05-xiaoxiao-v3.srt \
  --subtitle langfuse/captions/LF-05-xiaoxiao-v3.vtt \
  --shots langfuse/build/lf05-xiaoxiao-v3/timeline.json
```

输出：

```text
duration: format=173.071s audio=173.071s delta=0.000s
trailing_silence: 0.000s
subtitle LF-05-xiaoxiao-v3.srt: last_end=173.112s gap_to_video=-0.041s
subtitle LF-05-xiaoxiao-v3.vtt: last_end=173.112s gap_to_video=-0.041s
srt_vtt_last_delta: 0.000s
shots: 20 unique / 20 listed
PASS
```

## 抽帧看到的画面

| 秒 | 角标 | 构图 | 底部字幕 | 判定 |
|---:|---|---|---|---|
| 0 / 8 | 01/20 | hook | 一条漂亮样例，不等于可重复结论 | 同一镜，9.840 s，允许 |
| 16 | 02/20 | two-demo | 单条样例，解释不了整体差异 | 切镜 |
| 24 | 03/20 | dataset-card | Dataset：让实验回到同一组题 | 切镜；示意名 `intro-demo-v1` |
| 32 | 04/20 | item-grid | 每条 item 都有输入和明确的参考信息 | 切镜；脱敏占位 |
| 40 | 05/20 | id-tag | 结果要能追回原来的 item | 切镜；`item_demo_01` 示意 |
| 48 | 06/20 | input-output | 期望结果不能覆盖实际输出 | 切镜 |
| 56 | 07/20 | freeze-board | 先冻结数据和运行条件 | 切镜 |
| 64 | 08/20 | run-first | 第一次 run 保存原始输出和关联记录 | 切镜 |
| 72 | 09/20 | single-variable | 只改一个变量，差异才有解释起点 | 切镜 |
| 80 | 10/20 | run-second | 第二次 run 仍用同一 Dataset | 切镜 |
| 88 | 11/20 | comparison-table | 先逐条对照，再看汇总 | 切镜 |
| 96 | 12/20 | failure-focus | 平均分会掩盖关键样本回退 | 切镜 |
| 104 | 13/20 | score-attachment | Score 要能追到评分规则和对象 | 切镜 |
| 112 | 14/20 | run-metadata | 把这次 run 的条件完整留下 | 切镜 |
| 120 | 15/20 | trace-link | 低分背后要有可回看的 Trace | 切镜 |
| 128 / 136 | 16/20 | readback-loop | 回读同一轮的 Dataset、run 和 Score | 同一镜，9.672 s，允许 |
| 144 | 17/20 | boundary-gate | health 200 ≠ Dataset run 已完成 | 切镜 |
| 152 | 18/20 | representativeness | 固定样本 ≠ 样本有代表性 | 切镜 |
| 160 | 19/20 | stamp | prototype / L1：不是实验已跑通 | 切镜 |
| 168 / 172 | 20/20 | cta | 下一集：有了分数，能否直接上线？ | 同一镜，7.464 s，允许 |

接触表（本机临时文件，未入库）：

- `/tmp/lf05-independent-review/contact-1.jpg` … `contact-4.jpg`
- `/tmp/lf05-independent-review/mids-contact-1.jpg` … `mids-contact-4.jpg`

## 不能证明的范围

- 不能证明听感“有人味”。未逐秒听完整 173 秒。
- 不能证明当前实例已创建 Dataset、完成 run、写入 Score 或回读。画面里的 Dataset 名、item ID、分数连线都是示意。
- 不能证明播放器、manifest 或课程索引已经切到本文件。本任务未改这些文件。

## 建议下一步

1. 主 agent 可将本片登记为 LF-05 Xiaoxiao 原速样片，状态仍 `prototype / L1`。
2. 播放器优先链接 `LF-05-dataset-xiaoxiao-v3.mp4`。
3. 不把本 PASS 升级为 verified，也不把 health 200 / 示意 ID 写成真实 Dataset run。

交接格式完。
