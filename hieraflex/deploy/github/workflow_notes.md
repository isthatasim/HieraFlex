# GitHub Workflow Notes

## Branching
- Use feature branches for milestones (`codex/*` recommended).
- Keep each commit scoped to one subsystem.

## Suggested sequence
1. Scaffold and core infra
2. Data + replay + API
3. Agent + market logic
4. RL training/evaluation
5. Frontend dashboards
6. Docs + deployment assets

## CI suggestions
- Python lint/type checks
- Unit tests for data/replay/market/api/rl/deployment
- Optional frontend build check
