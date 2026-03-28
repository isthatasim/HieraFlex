# Agentic Design

## Community agent
Responsibilities:
- observe total and flexible demand
- detect congestion and peak risk
- compute coordination signal for houses
- evaluate fairness impact of savings/trades

## House agents
Each house is autonomous and runs:

1. Observe
2. Reason
3. Plan
4. Act
5. Reflect/Update

Decision inputs include price, demand, deadline slack, comfort slack, flexible ratio, optional DER states, and community signal.

## Appliance/resource controllers
Controllers enforce feasibility and integrity:
- non-interruptible cycle protection
- house-level cap enforcement
- battery/EV SOC bounds
- command acceptance/rejection feedback

## Explainability
Each action includes:
- dominant driver (`price`, `deadline`, `community`, `stability`)
- reward-term decomposition
- plain-English summary

## Fairness
Current implementation tracks Jain-style fairness and optional variance penalties in market coordination.
