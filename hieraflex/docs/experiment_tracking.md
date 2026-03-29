# Experiment Tracking

HieraFlex uses a lightweight, repository-local experiment tracker designed for resumable research runs and deployment portability.

## Storage layout
- `experiments/outputs/json/runs/<run_id>/run.json`
- `experiments/outputs/json/runs/<run_id>/metrics.jsonl`
- `experiments/outputs/json/runs/<run_id>/checkpoints.jsonl`
- `experiments/outputs/json/runs/<run_id>/evaluations.jsonl`
- `experiments/outputs/json/runs/<run_id>/worker.log`
- `experiments/outputs/json/runs/<run_id>/checkpoints/*.pt`

Additional publication outputs:
- `experiments/outputs/csv/`
- `experiments/outputs/parquet/`
- `experiments/outputs/figures/`
- `experiments/outputs/models/`

## Run metadata schema (core fields)
- `run_id`
- `algorithm`
- `config_path`
- `scenario_id`
- `status`
- `episodes_target`, `current_episode`, `current_step`
- `latest_checkpoint`, `best_checkpoint`
- `seed`, `price_mode`, `houses`
- `git_commit`
- timestamps (`created_at`, `started_at`, `ended_at`, `updated_at`)

## Comparison workflow
1. Fetch run list from `GET /training/runs`.
2. Request summaries with `POST /training/compare`.
3. Visualize best/latest/avg-last-10 return in the UI.
4. Export selected run artifacts for publication.

## Integrity and robustness
- duplicate run IDs are rejected at creation
- checkpoint path validation checks existence and non-empty file size
- running states are marked `interrupted` after backend restart
- runs can be resumed from latest or selected checkpoint

## Hugging Face artifact sync
Results can be published with:
```bash
python deploy/huggingface/publish_results.py --source experiments/outputs/json
```
Relative directory structure is preserved in the dataset repository (`results/...`), enabling multi-run comparisons in external demos.
