# HieraFlex Space (Docker)

This Space deploys **HieraFlex - Hierarchical Flexibility Intelligence for Community Energy Trading** in public demo mode.

## Runtime behavior
- FastAPI backend at `:7860`
- Built frontend bundle served from `/ui`
- Replay/inference and artifact inspection enabled
- Long uncontrolled public training disabled by deployment mode

## Environment defaults in Space image
- `HIERAFLEX_MODE=public-demo`
- `HIERAFLEX_SERVE_FRONTEND=1`
- `API_HOST=0.0.0.0`
- `API_PORT=7860`

## Required secrets for publishing flows
- `HF_TOKEN`
- `HF_DATASET_REPO_ID`
- `HF_MODEL_REPO_ID`
- `HF_SPACE_REPO_ID`
- `HF_USERNAME`

## Startup command
```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 7860
```
