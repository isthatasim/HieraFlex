# HieraFlex Space (Docker)

This Space hosts a public demo for **HieraFlex - Hierarchical Flexibility Intelligence for Community Energy Trading**.

## Runtime
- Docker Space
- Backend API + live replay WebSockets
- Optional frontend served separately or through reverse proxy

## Environment Variables
- `HF_TOKEN`
- `HF_DATASET_REPO_ID`
- `HF_MODEL_REPO_ID`
- `HF_SPACE_REPO_ID`
- `HF_USERNAME`

## Start
The Docker image starts:

```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port 7860
```
