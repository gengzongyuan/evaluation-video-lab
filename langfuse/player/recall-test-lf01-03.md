# LF-01–03 30 秒复述测试表

## 测试设计

每集找至少 1 名不了解 Langfuse 的测试者，只看视频前 30 秒，不读取脚本。播放后让其回答：

1. 这集要解决什么问题？
2. 你会做哪个具体动作？
3. 哪个结论仍不能从视频推出？

## 记录字段

```yaml
episode: LF-01|LF-02|LF-03
tester_id: "匿名编号"
watched_seconds: 30
answer_problem: ""
answer_action: ""
answer_boundary: ""
misunderstanding: ""
result: pass|revise|not_run
recorded_at: ""
```

## 通过标准

能准确复述本集问题和一个动作，且没有把“能记录/能回读”复述成“模型质量已证明”；否则修改前 30 秒钩子或证据边界字幕。
