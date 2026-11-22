# LF-04 Xiaoxiao 原速版独立验收

- 任务：LF04 成片独立音画复核
- 日期：2026-11-23（Asia/Shanghai）
- 对象：`langfuse/videos/LF-04-prompt-version-xiaoxiao-v3.mp4`
- 对照：`langfuse/captions/LF-04-xiaoxiao-v3.srt`、`langfuse/captions/LF-04-xiaoxiao-v3.vtt`、`langfuse/build/lf04-xiaoxiao-v3/timeline.json`、`langfuse/scripts/render_lf04_xiaoxiao_v3.py`
- 总评：**PASS（媒体合同）**
- 成熟度：保持 `prototype / L1`。本文件只证明原速旁白、切镜、烧录字幕和字幕同轴，不证明当前实例已创建 Prompt 版本、修改 label，或完成 Trace 回读。

制作方 QA `langfuse/lf04-xiaoxiao-v3-qa.md` 只作对照，不作为放行依据。下列数字全部由本任务重跑命令和看图得到。

## 结论

这版不是旧的 180 秒拉伸片，也不是 12 张 15 秒静卡。成片 166.866 秒，20 个唯一构图，单镜 7.104–9.768 秒，底部有烧录中文字幕，SRT/VTT 20 条时间轴和文本完全一致。自然旁白门退出码 0。

8 秒等间隔抽帧会在同一镜内落到两张相同画面（例如 0s/8s 都是 01/20，104s/112s 都是 14/20），这是因为这些镜头本身约 8.6–9.2 秒，不是跨镜冻帧。按 20 个镜头中点再抽一次，20 张内容哈希全部不同，第 7 镜 `trace-link` 也被看到。

不能把本 PASS 写成“听起来像真人”或“Langfuse 已验证”。质量门不听感，本环境也没有逐秒听完整片。

## 实测

| 检查 | 结果 | 证据 |
|---|---|---|
| 文件 | 存在 | 3,595,159 bytes |
| 封装时长 | 166.866 s | ffprobe format |
| 视频 | H.264 1080×1920 30 fps，166.833 s | ffprobe stream 0 |
| 音频 | AAC 24 kHz mono，166.848 s | ffprobe stream 1 |
| 音视频差 | 0.018 s | < 0.35 s 门限 |
| 尾部静音 | 0.000 s | 自然旁白门；`silencedetect=noise=-45dB:d=1.5` 无事件 |
| 响度 | mean -19.7 dB，max -2.2 dB | volumedetect |
| 拉伸 | 未发现 | 渲染器用 `edge-tts --rate=-5%`，单镜时长等于该镜音频时长，无 `atempo`/`setpts` |
| 镜头 | 20 unique / 20 listed | timeline + 自然旁白门 |
| 构图 | 20 种，相邻不重复 | hook → scattered → prompt-card → … → cta |
| 单镜时长 | 7.104–9.768 s | 全部落在 6–10 秒合同内 |
| 中点画面哈希 | 20/20 不同 | 独立计算，含被 8 秒网格漏掉的第 7 镜 |
| 烧录字幕 | 可见 | 每镜底部黑条中文；与 SRT 短句一致 |
| SRT/VTT | 20/20，时间轴和文本完全相同 | first 0.000，last 166.920；相对视频 gap -0.054 s |
| 乱码 / 敏感值 | 未发现 | 字幕、渲染器、分镜板无 U+FFFD、内网地址、Authorization、密钥赋值 |
| 自然旁白门 | PASS | 本任务重跑，退出码 0 |

质量门命令：

```bash
python3 langfuse/scripts/check_natural_voice_video.py \
  langfuse/videos/LF-04-prompt-version-xiaoxiao-v3.mp4 \
  --subtitle langfuse/captions/LF-04-xiaoxiao-v3.srt \
  --subtitle langfuse/captions/LF-04-xiaoxiao-v3.vtt \
  --shots langfuse/build/lf04-xiaoxiao-v3/timeline.json
```

输出：

```text
duration: format=166.866s audio=166.848s delta=0.018s
trailing_silence: 0.000s
subtitle LF-04-xiaoxiao-v3.srt: last_end=166.920s gap_to_video=-0.054s
subtitle LF-04-xiaoxiao-v3.vtt: last_end=166.920s gap_to_video=-0.054s
srt_vtt_last_delta: 0.000s
shots: 20 unique / 20 listed
PASS
```

## 抽帧看到的画面

8 秒网格（0–160，再加 166）用于找冻帧；中点抽帧用于确认 20 个构图都换过。

| 秒 | 角标 | 构图 | 底部字幕 | 判定 |
|---:|---|---|---|---|
| 0 / 8 | 01/20 | hook | Prompt 改一行，先问用了哪一版 | 同一镜，8.568 s，允许 |
| 16 | 02/20 | scattered | 散落各处的 Prompt，很难回溯 | 切镜 |
| 24 | 03/20 | prompt-card | 先给 Prompt 一个明确的名字和内容 | 切镜；示意名 `answer-guide-demo` |
| 32 | 04/20 | version-stack | 同一个 Prompt 名，也要区分具体版本 | 切镜 |
| 40 | 05/20 | label-road | label 指向版本，不代表效果更好 | 切镜 |
| 48 | 06/20 | code-fetch | 获取 Prompt → 填变量 → 交给模型 | 切镜 |
| 52.3 | 07/20 | trace-link | 让这次运行回指实际 Prompt 版本 | 8 秒网格漏掉，中点补看 |
| 56 | 08/20 | version-diff | 先看版本差异，再谈效果 | 切镜；质量栏空白 |
| 64 | 09/20 | label-warning | label 生效 ≠ 质量已验收 | 切镜 |
| 72 | 10/20 | run-boundary | 先锁定版本、时间和实际返回 | 切镜；字段均为占位 |
| 80 | 11/20 | fixed-input | 比较 Prompt，先固定同一条输入 | 切镜 |
| 88 | 12/20 | control-grid | 模型、参数、数据固定，只改 Prompt | 切镜 |
| 96 | 13/20 | score-split | 分数要连同样本和评分规则一起看 | 切镜；分数不填 |
| 104 / 112 | 14/20 | rollback | 版本帮助回滚，但不等于自动恢复 | 同一镜，9.192 s，允许 |
| 120 | 15/20 | checklist | 名称、版本、label、时间、内容都要核对 | 切镜 |
| 128 | 16/20 | not-equal | health 200 ≠ Prompt 已发布并回指 | 切镜 |
| 136 | 17/20 | loop | 用同一个 Trace ID 回读 Prompt 版本 | 切镜 |
| 144 | 18/20 | evidence-gate | 认证或字段失败，就停止放行 | 切镜 |
| 152 | 19/20 | stamp | prototype / L1：不是当前实例已发布 | 切镜 |
| 160 / 166 | 20/20 | cta | 下一集：用同一组样本做重复实验 | 同一镜，7.848 s，允许 |

接触表（本机临时文件，未入库）：

- `/tmp/lf04-independent-review/contact-1.jpg` … `contact-4.jpg`
- `/tmp/lf04-independent-review/mids-contact-1.jpg` … `mids-contact-4.jpg`

## 与旧 FAIL 的对照

| 旧阻断 | 本片 |
|---|---|
| 整段拉伸到 180 秒 | 166.866 秒，跟口播走 |
| 12 张约 15 秒静卡 | 20 镜，7–10 秒切一次 |
| 只有外挂字幕 | 画面内烧录，并保留同轴 SRT/VTT |
| 机械 `say` | 渲染脚本声线 `zh-CN-XiaoxiaoNeural`，`rate=-5%` |

镜内仍是静帧 PNG，没有流程动画。按当前 Xiaoxiao v3 合同（6–10 秒换构图 + 烧录字幕）可以通过；不能宣称已经做成运镜短视频。

## 不能证明的范围

- 不能证明听感“有人味”。未逐秒听完整 166 秒；LRA/音色未做人耳评分。
- 不能证明当前 Langfuse 实例已写入 Prompt、label 或 Trace。画面里的 `answer-guide-demo`、v1/v2、test/production、401/404 都是示意。
- 不能证明播放器、manifest 或课程索引已经切到本文件。本任务未改这些文件。

## 风险 / 缺口

- 主 agent 尚未把本片写入已验收清单。用户直接打开旧路径仍可能看到拉伸版或无字幕版。
- 8 秒抽帧不能单独当切镜证明，必须叠加分镜中点。
- 自然旁白门不检查构图是否真的不同，只数 shot id。本任务用中点哈希补了这一层。

## 建议下一步

1. 主 agent 可将本片登记为 LF-04 Xiaoxiao 原速样片，状态仍 `prototype / L1`。
2. 播放器优先链接 `LF-04-prompt-version-xiaoxiao-v3.mp4`，避免用户点到旧文件。
3. 不把本 PASS 升级为 verified，也不把 health 200 / 示意 ID 写成真实回读。

交接格式完。
