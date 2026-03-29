# HieraFlex

**Hierarchical Flexibility Intelligence for Community Energy Trading**

HieraFlex is a research-grade hierarchical agentic AI platform for community energy coordination with pseudo-real-time replay, house-level autonomy, market-aware control, and production-style web deployment.

## What This Stage Adds

- Live website deployment path (frontend + backend + worker split)
- Long-running PPO training jobs decoupled from the browser
- Resumable checkpoints with latest/best pointers
- Run registry + experiment tracking (JSON/JSONL)
- Training control and run comparison from UI
- Resource-level visual overlays (load, price, action context)
- Production and Hugging Face artifact publication flows

## Architecture

- **Frontend** (`frontend/`): dashboards, run control, comparisons, resource views
- **Backend API** (`backend/app/`): simulation, market, agent state, training APIs
- **Training worker** (`backend/app/worker_daemon.py`, `rl/training/training_worker.py`): long jobs/checkpoints/evaluation
- **Core engines** (`core/`): replay loop, market clearing, hierarchical agent logic
- **Experiment outputs** (`experiments/outputs/`): metrics, checkpoints, logs, artifacts

## Repository Layout

```text
hieraflex/
  backend/     FastAPI + services + websockets + training manager
  frontend/    React/Vite live dashboards and control panels
  core/        replay, market, agents, controllers, constraints
  data/        DEDDIAG adapters, preprocessing, schemas
  rl/          envs, PPO/baselines, training/evaluation
  experiments/ configs and tracked outputs
  deploy/      production + Hugging Face deployment assets
  docs/        formulation, lifecycle, deployment, visualization docs
  tests/       API, replay, market, RL env, deployment, training tests
```

## Quick Start

Python bootstrap:
```bash
cd hieraflex
python scripts/bootstrap.py
```

Frontend deps:
```bash
cd frontend
npm install
```

Run backend:
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

Run frontend:
```bash
cd frontend
npm run dev
```

## Live Website Deployment

Local production-like stack:
```bash
docker compose up --build
```

Production compose (nginx frontend + API + worker):
```bash
docker compose -f deploy/production/docker-compose.prod.yml up --build
```

Hugging Face Space / single-container demo UI is served from:
- `GET /ui`

## Long Training Workflows

Start from API:
```bash
curl -X POST http://localhost:8000/training/start \
  -H "Content-Type: application/json" \
  -d "{\"algorithm\":\"ppo_single\",\"config_path\":\"experiments/configs/single_house.yaml\",\"scenario_id\":\"demo_week\",\"episodes\":500}"
```

Stop:
```bash
curl -X POST http://localhost:8000/training/stop \
  -H "Content-Type: application/json" \
  -d "{\"run_id\":\"<RUN_ID>\"}"
```

Resume:
```bash
curl -X POST http://localhost:8000/training/resume \
  -H "Content-Type: application/json" \
  -d "{\"run_id\":\"<RUN_ID>\",\"extra_episodes\":200}"
```

Optional worker daemon:
```bash
python -m backend.app.worker_daemon
```

## Training Monitoring and Comparison

REST:
- `GET /training/status`
- `GET /training/runs`
- `GET /training/runs/{run_id}`
- `GET /training/runs/{run_id}/metrics`
- `GET /training/runs/{run_id}/checkpoints`
- `GET /training/runs/{run_id}/logs`
- `POST /training/compare`

WebSocket channels:
- `/ws/training_status`
- `/ws/training_metrics`
- `/ws/checkpoint_updates`

## Resource Visualization

Hierarchy:
- Community Live Dashboard
- House Live Dashboard
- Resource Dashboard
- Appliance Detail View

Resource endpoint:
- `GET /houses/{house_id}/resources?limit=240`

Signals include:
- house load
- appliance traces/states
- price overlays
- action context and replay-aligned demand dynamics

## Experiment Tracking Outputs

Per run:
- `experiments/outputs/json/runs/<run_id>/run.json`
- `experiments/outputs/json/runs/<run_id>/metrics.jsonl`
- `experiments/outputs/json/runs/<run_id>/checkpoints.jsonl`
- `experiments/outputs/json/runs/<run_id>/evaluations.jsonl`
- `experiments/outputs/json/runs/<run_id>/checkpoints/*.pt`
- `experiments/outputs/json/runs/<run_id>/worker.log`

## Hugging Face Integration (Optional)

Hugging Face is for hosting/sharing/demo artifacts, not the hard control loop.

Set `.env` vars:
- `HF_TOKEN`
- `HF_DATASET_REPO_ID`
- `HF_MODEL_REPO_ID`
- `HF_SPACE_REPO_ID`
- `HF_USERNAME`

Publish artifacts:
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

## Deployment Modes

- `local-dev`: fast iteration
- `local-prod`: dockerized local website
- `research-training`: long run execution with checkpointing
- `public-demo`: replay/inference focused safe website mode

## Tests

```bash
pytest -q
```

## Mathematical and RL Docs

- `docs/problem_formulation.md`
- `docs/mathematical_model.md`
- `docs/rl_formulation.md`
- `docs/training_lifecycle.md`
- `docs/deployment.md`
- `docs/live_website_mode.md`
- `docs/resource_visualization.md`
- `docs/experiment_tracking.md`
