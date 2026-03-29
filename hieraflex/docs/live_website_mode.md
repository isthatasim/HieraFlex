# Live Website Mode

Live website mode separates user-facing dashboards from long-running training execution.

## Architecture split
- Frontend app: visualization, controls, status, comparisons.
- Backend API: replay, market, agent state, run registry access.
- Worker daemon: training process lifecycle and recovery.
- Shared artifacts storage: checkpoints, logs, metrics, summaries.

## Public vs admin behavior
- Public demo mode: replay + inference + metrics viewing (read-only controls).
- Research/admin mode: start/stop/resume training and run comparison.

Use environment flag:
- `HIERAFLEX_MODE=public-demo` for safer public deployment.
- `HIERAFLEX_MODE=local-dev|local-prod|research-training` for internal work.

## Frontend resiliency behaviors
- loading and empty states for run/resource panels
- API error fallback without whole-page crash
- reconnect loop for WebSocket channels
- deployment banner indicating active mode and health
- worker-unavailable fallback to historical artifacts

## Live channels used by UI
- community stream
- house/action stream
- price stream
- training status stream
- training metrics stream
- checkpoint updates stream

## Non-blocking training guarantee
Training continues when:
- browser tab closes
- frontend container restarts
- client WebSocket disconnects

Run state remains recoverable from persisted run metadata and checkpoints.
