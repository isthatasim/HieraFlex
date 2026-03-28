from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SpaceRuntimeConfig:
    app_port: int = 7860
    demo_mode: bool = True
    enable_remote_inference: bool = False


def default_space_runtime_config() -> SpaceRuntimeConfig:
    return SpaceRuntimeConfig()
