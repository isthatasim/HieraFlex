from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
except Exception:  # pragma: no cover - optional dependency
    torch = None
    nn = None
    optim = None


@dataclass
class PPOConfig:
    obs_dim: int = 5
    action_dim: int = 8
    lr: float = 1e-3
    gamma: float = 0.99
    clip_eps: float = 0.2


class _Policy(nn.Module):
    def __init__(self, obs_dim: int, action_dim: int) -> None:
        super().__init__()
        self.net = nn.Sequential(nn.Linear(obs_dim, 64), nn.Tanh(), nn.Linear(64, 64), nn.Tanh())
        self.actor = nn.Linear(64, action_dim)
        self.critic = nn.Linear(64, 1)

    def forward(self, x):
        h = self.net(x)
        logits = self.actor(h)
        value = self.critic(h)
        return logits, value


class PPOAgent:
    def __init__(self, config: PPOConfig | None = None) -> None:
        self.config = config or PPOConfig()
        self.use_torch = torch is not None
        if self.use_torch:
            self.model = _Policy(self.config.obs_dim, self.config.action_dim)
            self.optimizer = optim.Adam(self.model.parameters(), lr=self.config.lr)
        else:
            self.weights = np.zeros((self.config.obs_dim, self.config.action_dim), dtype=float)

    def act(self, obs: np.ndarray) -> int:
        if self.use_torch:
            with torch.no_grad():
                x = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)
                logits, _ = self.model(x)
                probs = torch.softmax(logits, dim=-1).squeeze(0).numpy()
            return int(np.random.choice(len(probs), p=probs))
        logits = obs @ self.weights
        probs = np.exp(logits - np.max(logits))
        probs = probs / (np.sum(probs) + 1e-9)
        return int(np.random.choice(len(probs), p=probs))

    def update(self, batch: list[dict]) -> dict:
        if not batch:
            return {"loss": 0.0}
        returns = np.array([b["reward"] for b in batch], dtype=float)
        if self.use_torch:
            obs = torch.tensor(np.array([b["obs"] for b in batch]), dtype=torch.float32)
            actions = torch.tensor(np.array([b["action"] for b in batch]), dtype=torch.long)
            targets = torch.tensor(returns, dtype=torch.float32).unsqueeze(-1)
            logits, values = self.model(obs)
            logp = torch.log_softmax(logits, dim=-1)
            selected = logp.gather(1, actions.unsqueeze(-1)).squeeze(-1)
            advantage = (targets.squeeze(-1) - values.detach().squeeze(-1))
            policy_loss = -(selected * advantage).mean()
            value_loss = (values - targets).pow(2).mean()
            loss = policy_loss + 0.5 * value_loss
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            return {"loss": float(loss.item()), "policy_loss": float(policy_loss.item()), "value_loss": float(value_loss.item())}

        for sample in batch:
            self.weights[:, sample["action"]] += self.config.lr * sample["reward"] * sample["obs"]
        return {"loss": float(np.mean(np.abs(returns)))}

    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        if self.use_torch:
            torch.save({"state_dict": self.model.state_dict(), "config": self.config.__dict__}, path)
        else:
            path.write_text(json.dumps({"weights": self.weights.tolist(), "config": self.config.__dict__}, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: str | Path) -> "PPOAgent":
        path = Path(path)
        agent = cls()
        if not path.exists():
            return agent
        if torch is not None and path.suffix in {".pt", ".pth"}:
            payload = torch.load(path, map_location="cpu")
            cfg = PPOConfig(**payload.get("config", {}))
            agent = cls(cfg)
            agent.model.load_state_dict(payload["state_dict"])
            return agent
        payload = json.loads(path.read_text(encoding="utf-8"))
        cfg = PPOConfig(**payload.get("config", {}))
        agent = cls(cfg)
        agent.weights = np.array(payload["weights"], dtype=float)
        return agent
