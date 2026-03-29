from __future__ import annotations

import asyncio
import contextlib
import os
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from backend.app.services.checkpoint_service import checkpoint_service
from backend.app.services.experiment_tracker import experiment_tracker
from backend.app.services.io_utils import project_root, utc_now_iso
from backend.app.services.metrics_stream_service import metrics_stream_service
from backend.app.services.run_registry import run_registry
from backend.app.sockets.live_stream import live_stream_hub


@dataclass
class TrainingManager:
    root: Path = field(default_factory=project_root)
    active_processes: dict[str, subprocess.Popen] = field(default_factory=dict)
    monitor_task: asyncio.Task | None = None

    def __post_init__(self) -> None:
        run_registry.mark_recovered_states()

    def _python_exec(self) -> str:
        forced = os.getenv("HIERAFLEX_TRAIN_PYTHON")
        if forced:
            return forced
        return sys.executable

    def _worker_cmd(self, run: dict[str, Any], resume_from: str | None = None, extra_episodes: int | None = None) -> list[str]:
        cmd = [
            self._python_exec(),
            "-m",
            "rl.training.training_worker",
            "--run-id",
            run["run_id"],
            "--algorithm",
            run.get("algorithm", "ppo_single"),
            "--config",
            run.get("config_path", "experiments/configs/single_house.yaml"),
            "--scenario",
            run.get("scenario_id", "demo_week"),
            "--episodes",
            str(extra_episodes if extra_episodes is not None else run.get("episodes_target", 100)),
            "--seed",
            str(run.get("seed", 42)),
            "--checkpoint-interval",
            str(run.get("checkpoint_interval", 5)),
            "--eval-interval",
            str(run.get("eval_interval", 10)),
        ]
        if resume_from:
            cmd.extend(["--resume-from", resume_from])
        return cmd

    def _clear_stop_marker(self, run_id: str) -> None:
        stop_file = run_registry.run_dir(run_id) / "STOP"
        if stop_file.exists():
            stop_file.unlink()

    def start_run(self, payload: dict[str, Any]) -> dict[str, Any]:
        run = run_registry.create_run(
            {
                **payload,
                "status": "starting",
                "episodes_target": int(payload.get("episodes_target", payload.get("episodes", 100))),
                "checkpoint_interval": int(payload.get("checkpoint_interval", 5)),
                "eval_interval": int(payload.get("eval_interval", 10)),
            }
        )
        run_dir = run_registry.run_dir(run["run_id"])
        self._clear_stop_marker(run["run_id"])
        log_file = run_dir / "worker.log"
        cmd = self._worker_cmd(run)

        with log_file.open("a", encoding="utf-8") as f:
            f.write(f"[{utc_now_iso()}] Launching: {' '.join(cmd)}\n")

        proc = subprocess.Popen(
            cmd,
            cwd=str(self.root),
            stdout=log_file.open("a", encoding="utf-8"),
            stderr=subprocess.STDOUT,
        )
        self.active_processes[run["run_id"]] = proc
        return run_registry.update_run(run["run_id"], status="running", started_at=utc_now_iso(), pid=proc.pid)

    def stop_run(self, run_id: str) -> dict[str, Any]:
        run_dir = run_registry.run_dir(run_id)
        (run_dir / "STOP").write_text("stop requested", encoding="utf-8")
        proc = self.active_processes.get(run_id)
        if proc and proc.poll() is None:
            proc.terminate()
        return run_registry.update_run(run_id, status="stop_requested", stop_requested_at=utc_now_iso())

    def resume_run(self, run_id: str, checkpoint_path: str | None = None, extra_episodes: int = 50) -> dict[str, Any]:
        run = run_registry.load_run(run_id)
        if run.get("status") in {"running", "starting", "stop_requested"}:
            raise RuntimeError("Run is already active")

        resume = checkpoint_path or run.get("latest_checkpoint")
        self._clear_stop_marker(run_id)
        cmd = self._worker_cmd(run, resume_from=resume, extra_episodes=extra_episodes)
        log_file = run_registry.run_dir(run_id) / "worker.log"

        with log_file.open("a", encoding="utf-8") as f:
            f.write(f"[{utc_now_iso()}] Resuming: {' '.join(cmd)}\n")

        proc = subprocess.Popen(
            cmd,
            cwd=str(self.root),
            stdout=log_file.open("a", encoding="utf-8"),
            stderr=subprocess.STDOUT,
        )
        self.active_processes[run_id] = proc
        return run_registry.update_run(run_id, status="running", started_at=utc_now_iso(), pid=proc.pid)

    def sync_processes(self) -> None:
        finished: list[str] = []
        for run_id, proc in self.active_processes.items():
            code = proc.poll()
            if code is None:
                continue
            run = run_registry.load_run(run_id)
            status = run.get("status")
            if status not in {"completed", "stopped", "failed"}:
                if status == "stop_requested":
                    new_status = "stopped"
                else:
                    new_status = "completed" if code == 0 else "failed"
                run_registry.update_run(run_id, status=new_status, ended_at=utc_now_iso(), return_code=code)
            finished.append(run_id)
        for run_id in finished:
            self.active_processes.pop(run_id, None)

    async def _monitor_loop(self) -> None:
        while True:
            self.sync_processes()
            for run in run_registry.list_runs()[:25]:
                run_id = run["run_id"]
                polled = metrics_stream_service.poll(run_id)
                if polled["new_metrics"] or polled["new_checkpoints"] or run.get("status") in {"running", "starting", "failed", "completed"}:
                    await live_stream_hub.broadcast("training_status", {"run": run})
                    await live_stream_hub.broadcast(
                        "training_metrics",
                        {
                            "run_id": run_id,
                            "latest_metric": polled["latest_metric"],
                            "new_metrics": polled["new_metrics"],
                        },
                    )
                    if polled["new_checkpoints"]:
                        await live_stream_hub.broadcast(
                            "checkpoint_updates",
                            {"run_id": run_id, "new_checkpoints": polled["new_checkpoints"]},
                        )
            await asyncio.sleep(1.5)

    def start_monitoring(self) -> None:
        if self.monitor_task and not self.monitor_task.done():
            return
        self.monitor_task = asyncio.create_task(self._monitor_loop())

    async def stop_monitoring(self) -> None:
        if self.monitor_task and not self.monitor_task.done():
            self.monitor_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self.monitor_task

    def run_details(self, run_id: str) -> dict[str, Any]:
        run = run_registry.load_run(run_id)
        run["summary"] = experiment_tracker.summarize(run_id)
        run["latest_checkpoint_event"] = checkpoint_service.latest(run_id)
        run["best_checkpoint_event"] = checkpoint_service.best(run_id)
        return run


training_manager = TrainingManager()
