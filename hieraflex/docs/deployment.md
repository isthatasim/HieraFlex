# Deployment

HieraFlex supports separate website, API, and training worker execution. Public viewing and long training are intentionally decoupled.

## Deployment modes
1. `local-dev`: hot reload, editable code, direct API + frontend dev servers.
2. `local-prod`: dockerized frontend/backend/worker with persisted experiment outputs.
3. `research-training`: long jobs via API/CLI/worker daemon, browser optional.
4. `public-demo`: replay/inference focused, read-only training controls.

Set mode with `HIERAFLEX_MODE` in `.env`.
Set `HIERAFLEX_SERVE_FRONTEND=1` to serve bundled UI from backend `/ui`.

## Local development mode
Backend:
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

Optional background worker:
```bash
python -m backend.app.worker_daemon
```

## Local production mode
From project root (`hieraflex/`):
```bash
docker compose up --build
```

Services:
- `backend` on `:8000`
- `frontend` on `:5173`
- `training-worker` daemon (no public port)

## Production-style website bundle
Use production compose file:
```bash
docker compose -f deploy/production/docker-compose.prod.yml up --build
```

Services:
- API `:8000`
- Nginx frontend `:8080`
- Worker daemon

Persistent artifacts are stored under `experiments/outputs/...`.

## Training job control
Use API (browser can disconnect safely):
- `POST /training/start`
- `POST /training/stop`
- `POST /training/resume`
- `GET /training/runs`
- `GET /training/runs/{run_id}/metrics`
- `GET /training/runs/{run_id}/checkpoints`

WebSocket status streams:
- `/ws/training_status`
- `/ws/training_metrics`
- `/ws/checkpoint_updates`

## Hugging Face deployment support
Hugging Face is optional and not in the hard control loop.

Required env vars for publication:
- `HF_TOKEN`
- `HF_DATASET_REPO_ID`
- `HF_MODEL_REPO_ID`
- `HF_SPACE_REPO_ID`
- `HF_USERNAME`

Artifact publish commands:
```bash
python deploy/huggingface/publish_dataset.py --source experiments/outputs/parquet
python deploy/huggingface/publish_model.py --source experiments/outputs/models
python deploy/huggingface/publish_results.py --source experiments/outputs/json
python deploy/huggingface/publish_space.py --source deploy/huggingface
```

One-shot sync:
```bash
python deploy/huggingface/sync_to_hub.py
```

If variables are missing, publishing scripts fail with explicit setup guidance.

In Space Docker mode, the backend serves the built frontend bundle at `/ui`.
