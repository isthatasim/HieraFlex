# Training Lifecycle

HieraFlex training is orchestrated by backend services and worker processes, not by the browser session.

## Run states
- `queued`
- `starting`
- `running`
- `stop_requested`
- `stopped`
- `completed`
- `failed`
- `interrupted` (set on backend restart recovery)

## Lifecycle flow
1. `POST /training/start` creates run metadata (`run.json`) and launches a worker process.
2. Worker appends per-episode metrics (`metrics.jsonl`).
3. Every `checkpoint_interval`, worker saves checkpoint and appends checkpoint event (`checkpoints.jsonl`).
4. Every `eval_interval`, worker appends deterministic eval rows (`evaluations.jsonl`).
5. `POST /training/stop` creates a `STOP` marker and terminates process gracefully.
6. `POST /training/resume` relaunches from latest or selected checkpoint.

## Persisted run metadata
Location:
- `experiments/outputs/json/runs/<run_id>/run.json`

Fields tracked:
- run id, algorithm, scenario, config
- status and timestamps
- current episode and total steps
- latest and best checkpoint path
- checkpoint/evaluation intervals
- seed, price mode, houses
- git commit hash (when available)

## Checkpoint policy
- periodic save to `checkpoints/checkpoint_ep_XXXXX.pt`
- latest pointer: `latest_checkpoint`
- best pointer: `best_checkpoint`
- score basis: episodic return (can be extended to eval score)

## Resume semantics
- Resume from latest checkpoint by default.
- Optional explicit checkpoint path accepted by API.
- Existing `STOP` marker is cleared before worker restart.
- Interrupted runs are resumable after backend restart.

## Monitoring and observability
REST:
- `GET /training/status`
- `GET /training/runs`
- `GET /training/runs/{run_id}`
- `GET /training/runs/{run_id}/metrics`
- `GET /training/runs/{run_id}/checkpoints`
- `GET /training/runs/{run_id}/logs`
- `POST /training/compare`

Live channels:
- `/ws/training_status`
- `/ws/training_metrics`
- `/ws/checkpoint_updates`

## Selection of best model
Default:
\[
\theta^\*=\arg\max_{\theta_k \in \mathcal{C}} G(\theta_k)
\]
where \(G(\theta_k)\) is episodic return at checkpoint \(k\). Production pipelines can replace this with validation-score selection.

## Output layout
- `experiments/outputs/json/runs/<run_id>/run.json`
- `experiments/outputs/json/runs/<run_id>/metrics.jsonl`
- `experiments/outputs/json/runs/<run_id>/checkpoints.jsonl`
- `experiments/outputs/json/runs/<run_id>/evaluations.jsonl`
- `experiments/outputs/json/runs/<run_id>/checkpoints/*.pt`
- `experiments/outputs/json/runs/<run_id>/worker.log`
