# LAB-02 编码与证据文本审计（2026-11-22）

## 范围

本次审计覆盖 `evaluation-video-lab` 中可读的 Markdown、SRT、VTT、HTML 和 JSON 文本，重点检查 LAB-02 证据、质量记录和 LF-19/LF-20 课程资产。视频二进制和图片不属于文本编码扫描范围。

## 方法

在 `evaluation-video-lab` 根目录执行：

```bash
python3 - <<'PY'
from pathlib import Path

suffixes = {".md", ".srt", ".vtt", ".html", ".json"}
markers = (chr(0xfffd), chr(0x00ef)+chr(0x00bf)+chr(0x00bd), chr(0x00e2)+chr(0x20ac)+chr(0x2122), chr(0x00c3), chr(0x00c2))
for path in sorted(Path(".").rglob("*")):
    if not path.is_file() or path.suffix not in suffixes:
        continue
    text = path.read_text(encoding="utf-8")
    hits = [m for m in markers if m in text]
    if hits:
        print(path, hits)
print("encoding scan complete")
PY
```

同时检查文本是否能以 UTF-8 解码，并用 `git diff` 复核修复只改变损坏的文字，不改变证据结论、状态或命令。

## 结果

- UTF-8 解码：PASS；扫描到的文本文件均可读取。
- 常见乱码标记：PASS；修复前发现 21 个文本文件含替换字符或明显的 UTF-8 乱码片段，已按上下文恢复为可读中文。
- LAB-02 关键证据文本：PASS；`lf19-evidence-audit-2026-11-22.md`、`lf01-03-recording-form.md`、`lf13-15-recording-form.md` 与 `docs/quality/lab02-credentials-audit.md` 的证据状态和敏感信息边界未改变。
- 原始响应完整性：不受影响；`evidence/raw/` 下 JSON 正文和 `SHA256SUMS-2026-11-22.txt` 未修改。
- 凭据边界：不受影响；本次只修复编码，不添加项目 key、secret、Authorization header 或请求体。

## 修复示例

- 受保护凭据、业务上下文、录制表标题、Trace 和查询等文字恢复为正常 UTF-8 中文。
- 修复只处理替换字符和乱码片段，未改动状态值、命令、URL 或证据结论。

## 边界

本审计证明的是当前工作区文本可读性和修复差异，不证明图片、视频字幕渲染、字体覆盖或外部平台显示效果。发布前仍需对导出视频和平台草稿做一次视觉检查。
