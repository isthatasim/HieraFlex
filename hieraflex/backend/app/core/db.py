from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class InMemoryDB:
    sessions: dict[str, dict] = field(default_factory=dict)
    training_jobs: dict[str, dict] = field(default_factory=dict)
    evaluation_jobs: dict[str, dict] = field(default_factory=dict)
    results: dict[str, dict] = field(default_factory=dict)


db = InMemoryDB()
