# LF-01 v2 / LF-02 v2 内容与字幕审计

审计日期：2026-11-22（Asia/Shanghai）

## 结论

两条 v2 样片的课程主线和证据边界基本清楚，且 QA 记录证明了媒体层面的快切、非静音和多点抽帧。但当前字幕资产仍有一个阻断级问题：LF-02 SRT/VTT 的时间码把 15 秒写成了 `00:15:00,000` / `00:15:00.000`，这表示 15 分钟而不是 15 秒，无法与 180 秒视频同步。修复字幕时间码并清除乱码后，才能进入字幕发布门。

## 已核对范围

- `langfuse/videos/LF-01-langfuse-overview-v2.mp4`
- `langfuse/videos/LF-02-trace-v2.mp4`
- `langfuse/captions/LF-01-v2.srt/.vtt`
- `langfuse/captions/LF-02-v2.srt/.vtt`
- `langfuse/lf01-v2-qa.md`
- `langfuse/lf02-v2-qa.md`

## 通过项

| 项目 | 结果 | 依据 |
|---|---|---|
| LF-01/LF-02 镜头节奏 | `PASS`（媒体层） | 两条 QA 均记录 12 个约 15 秒镜头 |
| 多点画面变化 | `PASS`（媒体层） | QA 记录 0/15/30/60/120/165 秒抽帧；主 agent 对样片做过抽帧复核 |
| 音频非静音 | `PASS`（媒体层） | LF-01 mean -26.0/max -1.7 dB；LF-02 QA 记录 volumedetect 非静音 |
| 证据边界 | `PASS` | 两条均保留 `prototype / L1`，明确不证明当前 Trace 写入或回读 |
| 主要概念方向 | `PASS（待官方版本复核）` | Trace/Span/Generation 的概念链路与现有课程脚本一致 |

## 阻断问题

### LF-02 字幕时间码错误

当前 `langfuse/captions/LF-02-v2.srt` 和 `.vtt` 的片段写成：

```text
00:00:00,000 --> 00:15:00,000
...
00:15:00,000 --> 00:30:00,000
```

应为每 15 秒一段的格式：

```text
00:00:00,000 --> 00:00:15,000
00:00:15,000 --> 00:00:30,000
```

这项必须由字幕制作者修复后重新运行时间码检查；本审计不直接改字幕文件，避免越过责任边界。

### LF-02 字幕乱码

第 4 段包含 `Span ��黑箱变成一棵有层次的调用树`。应根据口播原文核对为“Span 把黑箱变成一棵有层次的调用树”，并重新检查 UTF-8。乱码会直接降低可发布性。

## 证据与断言边界

- “Trace 把一次请求的步骤关联起来”可作为概念讲解，但当前不是本实例新 Trace 的实测证明。
- “健康检查和历史截图不能当作当前新 Trace”与 LAB-02 契约一致，可保留。
- `Trace 只能说明调用被记录了，不能自动证明答案正确`是边界说明，可保留。
- `Generation` 的字段、Observation 类型和当前 v4 API 细节，录制前仍需复核官方当前文档；字幕不应写成当前实例已回读。
- 两条样片都应继续标记 `prototype / L1`。

## 待办与放行条件

1. 修复 LF-02 SRT/VTT 的所有时间码为 15 秒分段。
2. 修复 LF-02 字幕乱码并跑 UTF-8/乱码扫描。
3. 用脚本检查时间码单调递增、总时长不超过 180 秒，并逐条验证字幕文件非空。
4. 修复后重新打开播放器抽查 LF-02 的 0、15、30 秒字幕同步。
5. 在以上事项完成前，LF-02 v2 的媒体门可以是 `PASS`，字幕发布门保持 `BLOCKED`。

## 复核命令

```bash
python3 - <<'PY'
from pathlib import Path
import re
for p in (Path('langfuse/captions/LF-01-v2.srt'), Path('langfuse/captions/LF-02-v2.srt')):
    text=p.read_text(encoding='utf-8')
    assert '\ufffd' not in text, p
    for line in text.splitlines():
        if '-->' in line:
            assert re.match(r'^\d\d:\d\d:\d\d,\d{3} --> \d\d:\d\d:\d\d,\d{3}$', line), (p,line)
print('caption syntax/UTF-8 scan: PASS')
PY
```
