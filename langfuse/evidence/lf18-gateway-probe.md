# LF-18 Gateway 探针证据

来源：`evidence/runtime-discovery-2026-11-22-0044.md`。

- Gateway `/health`：HTTP 200，`{"status":"ok"}`。
- Gateway `/ready`：HTTP 503，`{"status":"unconfigured"}`。

探针没有修改配置、发送模型请求或写入 Trace。它只能支持“进程存活”和“配置未就绪”的区分，不能诊断具体缺少哪个 provider/service key，也不能证明 Gateway 生产安全。
