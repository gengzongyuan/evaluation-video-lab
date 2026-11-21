# LF-13–15 ��实录制表

| 集数 | 必填证据 | 放行条件 | 阻塞条件 |
|---|---|---|---|
| LF-13 自托管 | Web/Worker/DB/对象存储 health、版本、重启恢复、备份演练 | 链路组件与版本可回指 | 只验证页面可开 |
| LF-14 版本 | server/SDK/CLI/runtime、lockfile hash、文档日期、最小运行日志 | 代码、运行物、脚本一致 | latest 或版本未知 |
| LF-15 发布门 | 脚本、成片、原始素材、脱敏报告、manifest、回滚 commit、复述测试 | 每条断言有来源/运行证据，能回滚 | 泄密、无证据或不可回滚 |

## 公共填写字段

```yaml
recorded_at: ""
langfuse_version: ""
sdk_version: ""
git_commit: ""
source_urls: []
raw_evidence_dir: ""
redaction_check: "PASS|FAIL"
rollback_ref: ""
status: "prototype|verified|ready|blocked"
blocker: ""
```

health `OK` 只能证明端点在核验时可用；不自动证明写入、权限、备份恢复或生产安全。
