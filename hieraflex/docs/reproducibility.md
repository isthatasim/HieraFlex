# Reproducibility

## Data assumptions
- DEDDIAG is primary appliance trace backbone.
- Reference alignment: DEDDIAG loader metadata indicates multi-home, long-duration, high-frequency appliance traces with event annotations; HieraFlex preserves that measured appliance structure.
- If unavailable, synthetic fallback traces are generated and tagged as `source=synthetic`.
- Price stream is generated reproducibly from fixed seed unless external tariff stream is provided.

## Experiment reproducibility
- Scenario configs in `experiments/configs/*.yaml`
- Reward weights in `experiments/configs/reward_weights.yaml`
- Training logs in `experiments/outputs/logs`
- Evaluation exports in CSV/Parquet/JSON
- Deterministic dependency lock in `requirements-lock.txt`
- One-command environment bootstrap via `python scripts/bootstrap.py`

## Suggested protocol
1. Freeze config snapshot.
2. Run replay baseline.
3. Train PPO with fixed seed.
4. Evaluate against baseline agents.
5. Export outputs and figures.
6. Publish dataset/model artifacts.
