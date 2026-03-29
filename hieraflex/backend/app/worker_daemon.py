from __future__ import annotations

import logging
import time

from backend.app.services.run_registry import run_registry
from backend.app.services.training_manager import training_manager


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | worker | %(message)s")
    logging.info("HieraFlex training worker daemon started")
    while True:
        training_manager.sync_processes()
        runs = run_registry.list_runs()
        active = [r for r in runs if r.get("status") in {"running", "starting", "stop_requested"}]
        logging.info("active_runs=%s total_runs=%s", len(active), len(runs))
        time.sleep(5)


if __name__ == "__main__":
    main()
