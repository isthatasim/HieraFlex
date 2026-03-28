# Deployment

## Local deployment

```bash
cd hieraflex
python -m pip install -e .[test,rl]
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Docker compose:

```bash
cd hieraflex
docker compose up --build
```

## Hugging Face deployment

1. Set `.env` variables based on `.env.example`.
2. Publish artifacts:

```bash
python deploy/huggingface/publish_dataset.py --source experiments/outputs/parquet
python deploy/huggingface/publish_model.py --source experiments/outputs/models
python deploy/huggingface/publish_space.py --source deploy/huggingface
```

3. Or run one-shot sync:

```bash
python deploy/huggingface/sync_to_hub.py
```

If tokens are missing, scripts fail with explicit instructions.
