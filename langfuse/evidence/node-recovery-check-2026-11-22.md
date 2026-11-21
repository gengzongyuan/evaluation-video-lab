# Node recovery check — 2026-11-22

## Scope

This is a read-only precheck for the Langfuse 4.79.0 instance documented in `LANGFUSE_DEPLOYED_INSTANCE_172.16.33.136.md`. It does **not** claim that a Compose restart or a host reboot was completed.

## Observed from the recording workstation

| Endpoint | Result | Interpretation |
|---|---|---|
| `http://172.16.33.136:3000/api/public/health?failIfDatabaseUnavailable=true` | HTTP 200, `{"status":"OK","version":"4.79.0"}` | Web endpoint and its database check responded at probe time. |
| `http://172.16.33.136:3000/api/public/ready` | HTTP 200, `{"status":"OK","version":"4.79.0"}` | Web readiness endpoint responded at probe time. |
| `http://172.16.33.136:3031/health` | HTTP 200, `{"status":"ok"}` | Gateway process health responded. |
| `http://172.16.33.136:3031/ready` | HTTP 503, `{"status":"unconfigured"}` | Gateway is not configured for a usable model-request path. |
| `http://172.16.33.136:9090/minio/health/live` | HTTP 200 | MinIO liveness endpoint responded. |

The probes were run on 2026-11-22 (Asia/Shanghai) with `curl --max-time 8`. These results are point-in-time endpoint checks; they do not prove trace ingestion, worker consumption, backup validity, or restart recovery.

## Recovery action attempted

The documented SSH command was attempted in batch mode:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=8 work@172.16.33.136 \
  'cd /home/work/langfuse && docker compose -f docker-compose.yml -f docker-compose.server.yml ps --format json'
```

It failed before command execution with:

```text
Permission denied (publickey,gssapi-keyex,gssapi-with-mic,password).
```

No remote service was restarted, stopped, rebuilt, pulled, or modified. No host reboot was attempted.

## Status and next action

`status: blocked` for node-recovery evidence. An operator with the documented SSH access (or an approved equivalent read-only access path) must run the Compose restart check from the deployment runbook, then capture:

1. `docker compose ... ps` showing all expected services healthy;
2. the Web health response with `status=OK` and `version=4.79.0` after restart;
3. Web ready and Worker health responses;
4. application container restart counts and relevant logs;
5. whether the check was a service restart or a full host reboot.

Until those are captured, retain the existing documentation's boundary: the instance is healthy at the sampled endpoints, while restart recovery and backup restoration remain unverified.
