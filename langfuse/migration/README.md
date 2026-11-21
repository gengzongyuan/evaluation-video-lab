# LF-16 v4 OTEL migration reference

These snippets are reference material extracted from the locally archived official Langfuse SDK overview, not a successful run. They contain no real keys and use redacted input/output.

## Python

`python_v5_trace.py` follows the archived official Python SDK v5 shape: `get_client()`, nested `start_as_current_observation`, `generation`, and `flush()`. Run only after installing the pinned current SDK and setting protected environment variables.

Official references to recheck at recording time:

- https://langfuse.com/docs/observability/sdk/overview
- https://langfuse.com/docs/observability/sdk/upgrade-path/python-v4-to-v5
- https://langfuse.com/integrations/native/opentelemetry/migration-to-v4

## JavaScript/TypeScript

The archived official guide uses `@langfuse/tracing`, `@langfuse/otel`, `@opentelemetry/sdk-node`, `LangfuseSpanProcessor`, and `sdk.shutdown()` for short-lived processes. Do not copy package versions from this repository without rechecking the current compatibility page.

## Safety

- Never put keys in this repository, video, shell history, or evidence JSON.
- Use a new redacted case ID and save the SDK/server versions.
- A successful OTEL HTTP response is not enough: obtain a new Trace ID and UI/API readback.
