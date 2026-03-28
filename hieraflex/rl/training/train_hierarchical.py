from __future__ import annotations

import argparse
import json

from rl.training.train_multi_house_shared_ppo import run_shared_training
from rl.training.train_single_house import run_training


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="experiments/configs/hierarchical.yaml")
    args = parser.parse_args()
    single = run_training(args.config)
    shared = run_shared_training(args.config)
    print(json.dumps({"single": single, "shared": shared}, indent=2))
