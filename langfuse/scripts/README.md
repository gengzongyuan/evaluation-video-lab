# Langfuse 运行脚本

## `check-runtime.sh`

在受保护 shell 中运行：

```bash
export LANGFUSE_BASE_URL='https://your-langfuse.example'
export LANGFUSE_PUBLIC_KEY='pk-...'
export LANGFUSE_SECRET_KEY='sk-...'
./check-runtime.sh
```

脚本只输出变量是否存在、health 状态和服务端版本，绝不打印 key 值。退出码：

- `0`：变量齐全且 health 为 OK
- `2`：变量缺失
- `3`：health 非 OK

当前仓库没有内置任何真实 key；不要把 `.env`、终端输出或 API 响应加入 Git。
