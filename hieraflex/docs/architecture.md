# HieraFlex Architecture

**HieraFlex (Hierarchical Flexibility Intelligence for Community Energy Trading)** is implemented as a 3-layer agentic system:

1. **Upper layer: Community agent + market coordinator**
2. **Middle layer: Autonomous house agents**
3. **Lower layer: Appliance/resource safety controllers**

## Runtime dataflow

1. DEDDIAG appliance traces are loaded and cleaned.
2. Replay engine emits pseudo-real-time events with injected prices.
3. House agents run observe/reason/plan/act per step.
4. Market engine collects bids/offers and clears local trades.
5. Community agent publishes fairness-aware coordination signal.
6. Backend emits live WebSocket channels and persists outputs.
7. Frontend renders community, house, and appliance drill-down views.

## Modules

- `data/`: ingestion, cleaning, feature construction, scenario windows, price generation
- `core/replay/`: event clock, replay engine, event bus
- `core/agents/`: community, house, appliance logic + memory/planner/explainer
- `core/market/`: tariff, bid/offer, matching, clearing
- `backend/app/`: API, service orchestration, live channels
- `rl/`: environments, baselines, PPO training/evaluation
- `deploy/huggingface/`: dataset/model/space publishing utilities

## Control-loop principle

Real-time control runs locally in backend services. Hugging Face is used only for artifact hosting, optional demo inference, and Space deployment.
