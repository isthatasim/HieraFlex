from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def export(input_dir: str, output: str) -> dict:
    input_path = Path(input_dir)
    out_path = Path(output)
    out_path.mkdir(parents=True, exist_ok=True)
    generated = []
    for csv_file in input_path.glob("*.csv"):
        df = pd.read_csv(csv_file)
        pq_path = out_path / f"{csv_file.stem}.parquet"
        df.to_parquet(pq_path, index=False)
        generated.append(str(pq_path))
    return {"generated": generated}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    print(export(args.input, args.output))
