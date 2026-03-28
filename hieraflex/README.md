# HieraFlex

**Hierarchical Flexibility Intelligence for Community Energy Trading**

HieraFlex is a research-grade, hierarchical, agentic AI platform for pseudo-real-time community energy trading and appliance-level load management. It replays DEDDIAG-style appliance traces as live streams, runs autonomous house agents continuously against dynamic prices, coordinates local trading at community level, and exposes explainable decisions from community down to appliance level.

## Core Capabilities

- Hierarchical control stack (community -> house -> appliance/resource)
- Continuous observe/reason/plan/act loops per house
- Price-responsive scheduling and re-planning during replay
- Pseudo-real-time event replay with pause/resume/reset/seek/speed
- Local market engine with bids/offers, matching, and local clearing
- Baselines: no-control, rule-based, cheapest-slot, PPO
- Evaluation pipeline with cost, PAR, fairness, trading, responsiveness metrics
- FastAPI backend + WebSocket live channels
- React frontend with hierarchical drill-down dashboards
- Hugging Face support for dataset/model/Space publication (optional)

## DEDDIAG Backbone Assumptions

HieraFlex ingestion is aligned with the DEDDIAG loader ecosystem assumptions: appliance-level traces across multiple homes, long-horizon household recordings, and event-style appliance annotations. The loader in `data/loaders/deddiag_adapter.py` preserves measured appliance traces when present and only adds clearly tagged synthetic signals (`source=synthetic`) when required for missing exogenous variables (e.g., tariff, DER, market fields).

## Repository Structure

```text
hieraflex/
  backend/           # FastAPI backend, services, runtime orchestration
  frontend/          # React + Vite dashboards
  core/              # Replay, market, agents, control, constraints
  data/              # DEDDIAG adapters, preprocessing, schema models
  rl/                # Envs, PPO and baseline agents, training/evaluation
  experiments/       # Configs + outputs
  deploy/            # Hugging Face + GitHub deployment assets
  docs/              # Formulation, architecture, deployment, reproducibility
  tests/             # Unit tests
```

## Architecture Overview

### Upper layer: Community
- monitors total/flexible demand and congestion
- computes fairness-aware coordination signal
- coordinates local market clearing with residual grid settlement

### Middle layer: House agents
- observe prices, flexibility, deadlines, comfort slack, and community signal
- reason about cost/flexibility/comfort/trade opportunity
- plan short-horizon actions and re-plan online
- produce explanation payloads for every decision

### Lower layer: Appliance/resource controllers
- enforce non-interruptibility, SOC bounds, and house-cap feasibility
- accept/reject commands with safety feedback

## Mathematical and RL Formulation

Full research formulation is documented in:
- `docs/notation.md`
- `docs/problem_formulation.md`
- `docs/mathematical_model.md`
- `docs/rl_formulation.md`
- `docs/market_design.md`

Includes:
- sets, indices, parameters, decision variables
- household balance and scheduling constraints
- battery/EV/PV models (toggleable)
- local trading constraints and clearing model
- community and house objectives
- fairness formulations (variance and Jain index)
- MDP definition, reward decomposition, and baseline rules

## Installation

Python: `3.10+` (recommended `3.11`)

```bash
cd hieraflex
python scripts/bootstrap.py
```

On Windows, if your default `python` is older, bootstrap automatically uses `py -3.11` when available.

Optional frontend:

```bash
python scripts/bootstrap.py --with-frontend
```

Optional RL/Hugging Face extras:

```bash
python scripts/bootstrap.py --with-optional
```

Deterministic lock files: `requirements-lock.txt`, `requirements-lock-optional.txt`

## Local Run

Backend API:

```bash
cd hieraflex
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

Frontend:

```bash
cd hieraflex/frontend
npm run dev
```

Docker compose:

```bash
cd hieraflex
docker compose up --build
```

## Replay Mode

Start replay:

```bash
curl -X POST http://localhost:8000/simulation/start \
  -H "Content-Type: application/json" \
  -d '{"scenario_id":"demo_week","start_index":0,"end_index":288,"replay_speed":60}'
```

Control:
- `POST /simulation/pause`
- `POST /simulation/reset`
- `POST /simulation/seek`

WebSocket channels:
- `/ws/community`
- `/ws/houses`
- `/ws/actions`
- `/ws/trades`
- `/ws/price`
- `/ws/training` (reserved stream)

## API Summary

- `GET /houses`
- `GET /houses/{id}`
- `GET /houses/{id}/agent-state`
- `GET /appliances`
- `GET /market/state`
- `POST /simulation/start|pause|reset|seek`
- `POST /training/start`
- `GET /training/status`
- `POST /evaluation/run`
- `GET /results/summary`
- `GET /results/export`
- `GET /deployment/status`

## Training and Evaluation

Train single-house PPO:

```bash
python -m rl.training.train_single_house --config experiments/configs/single_house.yaml
```

Train shared multi-house PPO:

```bash
python -m rl.training.train_multi_house_shared_ppo --config experiments/configs/community.yaml
```

Run baseline comparison:

```bash
python -m rl.evaluation.compare_agents --config experiments/configs/community.yaml
```

Exports:
- CSV: `experiments/outputs/csv/`
- Parquet: `experiments/outputs/parquet/`
- JSON summaries/logs: `experiments/outputs/logs/`

## Frontend Views

- **Community Overview**: demand, flexible load, trade volume, clearing price, fairness
- **House Agent Detail**: action/state/reason per house
- **Resource Layer**: mains/appliances/DER/grid-trade traces
- **Appliance Explorer**: appliance-level characteristics and control context
- **Training Dashboard**: training status and curves payload
- **Evaluation Dashboard**: baseline vs PPO metrics
- **Scenario Builder**: scenario and mode controls
- **Explainability Panel**: decision reason and reward drivers

## Hugging Face Integration

Hugging Face is support-only (hosting/distribution/demo), not hard control loop.

Environment variables (`.env`):
- `HF_TOKEN`
- `HF_DATASET_REPO_ID`
- `HF_MODEL_REPO_ID`
- `HF_SPACE_REPO_ID`
- `HF_USERNAME`

Publish dataset/model/space:

```bash
python deploy/huggingface/publish_dataset.py --source experiments/outputs/parquet
python deploy/huggingface/publish_model.py --source experiments/outputs/models
python deploy/huggingface/publish_space.py --source deploy/huggingface
```

One-shot sync:

```bash
python deploy/huggingface/sync_to_hub.py
```

If tokens are missing, scripts fail gracefully with actionable messages.

## Testing

```bash
cd hieraflex
pytest -q
```

Coverage includes data loading, replay engine, market engine, house agent loop, API routes, RL env, and deployment config checks.

If you need to rebuild a clean environment, rerun:

```bash
python scripts/bootstrap.py
```

## Research Positioning

HieraFlex is designed for:
- reproducible demand response experiments
- community trading and fairness studies
- hierarchical multi-agent control research
- deployment-ready demos with optional public artifact sharing

It cleanly separates:
- measured appliance traces
- engineered features
- simulated exogenous variables (e.g., synthetic tariff)
- optimization/RL outputs
- deployment artifacts
