# Hugging Face Integration

HieraFlex treats Hugging Face as a support layer for:
- dataset hosting/streaming
- model checkpoint distribution
- public demo deployment via Spaces

## Not for hard control
Observe/reason/plan/act loops, market clearing, and replay synchronization run locally in backend runtime.

## Dataset publishing
`deploy/huggingface/publish_dataset.py` uploads parquet scenario shards and dataset card.

## Model publishing
`deploy/huggingface/publish_model.py` uploads PPO checkpoints, config, and model card.

## Space publishing
`deploy/huggingface/publish_space.py` uploads Docker Space package.

## Optional remote inference
Can be enabled only for demo/benchmark mode, not required for core control.
