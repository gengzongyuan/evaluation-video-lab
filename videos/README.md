# 视频原型

本目录包含两条 **180 秒、9:16、可播放** 的视频原型：

- `video-01-model-rankings-prototype.mp4`：模型排行榜的三问法
- `video-02-minimal-eval-prototype.mp4`：四格最小评测

当前原型使用深色竖屏画面与中文旁白音轨，口播来自对应脚本，所有数字均按“示意数据”处理。它们用于验证时长、画幅、音轨和内容顺序，不能直接当作最终发布成片。下一步制作应替换为真实录屏、证据卡、失败样本、字幕和剪辑镜头。

验证命令：

```bash
ffprobe -v error -show_entries format=duration,size -of default=nw=1 video-*.mp4
```

预期：两条视频 `duration=180.000000`，画面为 1080×1920。
