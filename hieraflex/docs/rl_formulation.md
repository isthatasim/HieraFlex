# RL Formulation

HieraFlex models each house as an autonomous policy in a multi-agent environment with optional shared-policy training.

## MDP / Markov game structure
- State space \(\mathcal{S}\): local house state + community signal + replay context.
- Action space \(\mathcal{A}\): appliance start/defer/keep, battery/EV charge controls, bid/offer decisions, no-op.
- Transition \(\mathcal{P}(s_{t+1}\mid s_t, a_t)\): induced by replay traces, controller feasibility, market clearing, and exogenous price process.
- Reward \(r_{h,t}\): weighted decomposition of cost, comfort, violations, and flexibility value.
- Discount factor \(\gamma \in (0,1)\).

## House observation vector
\[
s_{h,t}=
[\text{clock},\pi_t,\pi_{t-w:t},\hat \pi_{t:t+H},
P_{h,t}^{load}, \text{rolling load},
\text{appliance states}, \text{remaining cycle},
\text{deadline slack}, \text{community signal},
\text{trade signal}, \text{DER state}, \text{action history}]
\]

## Reward decomposition
\[
r_{h,t}=
-\alpha_1 C_{h,t}^{energy}
-\alpha_2 C_{h,t}^{peak}
-\alpha_3 C_{h,t}^{comfort}
-\alpha_4 C_{h,t}^{switch}
-\alpha_5 C_{h,t}^{deadline}
-\alpha_6 C_{h,t}^{violation}
+\alpha_7 Rev_{h,t}^{trade}
+\alpha_8 R_{h,t}^{self}
+\alpha_9 R_{h,t}^{flex}
+\alpha_{10}R_{h,t}^{resp}
\]

All \(\alpha\) coefficients are configurable in YAML (`experiments/configs/reward_weights.yaml`).

## PPO objective (high-level)
For policy \(\pi_\theta\), old policy \(\pi_{\theta_{old}}\), and advantage \(\hat A_t\):
\[
L^{clip}(\theta)=
\mathbb{E}_t\left[
\min\left(
r_t(\theta)\hat A_t,\,
\text{clip}(r_t(\theta),1-\epsilon,1+\epsilon)\hat A_t
\right)
\right]
\]
with
\[
r_t(\theta)=\frac{\pi_\theta(a_t\mid s_t)}{\pi_{\theta_{old}}(a_t\mid s_t)}
\]

Value and entropy terms:
\[
L(\theta)=L^{clip}(\theta)-c_vL^{value}(\theta)+c_e\mathcal{H}(\pi_\theta)
\]

## Long-horizon training lifecycle
For episode \(e\):
\[
G_e=\sum_{t=0}^{T_e-1}\gamma^t r_t
\]
Training objective:
\[
\max_\theta \mathbb{E}_{e\sim \mathcal{D}_{train}}[G_e]
\]

Checkpoint score (default):
\[
Score_{ckpt}=\frac{1}{|\mathcal{E}_{eval}|}\sum_{e\in\mathcal{E}_{eval}} G_e
\]
Best model:
\[
\theta^\*=\arg\max_{\theta_k\in\mathcal{C}} Score_{ckpt}(\theta_k)
\]

## Baselines
1. Historical no-control (`FixedScheduleAgent`)
2. Rule-based price-responsive (`RuleBasedAgent`)
3. Cheapest-slot heuristic (`CheapestSlotAgent`)
4. PPO (`PPOAgent`)

## Evaluation metrics
- Total cost:
\[
Cost=\sum_{h,t}\left(\pi_t^{buy}P_{h,t}^{grid,in}-\pi_t^{sell}P_{h,t}^{grid,out}\right)
\]
- Savings:
\[
Savings_h=Cost_h^{baseline}-Cost_h^{policy}
\]
- Peak-to-average ratio:
\[
PAR=\frac{\max_t P_t^{comm}}{\frac{1}{|\mathcal{T}|}\sum_t P_t^{comm}}
\]
- Price response efficiency:
\[
PRE=-corr(\pi_t,\Delta P_t^{flex})
\]
- Smoothed learning curve (EMA):
\[
\tilde G_e=\beta \tilde G_{e-1} + (1-\beta)G_e
\]
- Decision update frequency:
\[
f_{update}=\frac{\#\text{decision updates}}{\text{wall-clock duration}}
\]
- Inference latency:
\[
L_{inf}=\frac{1}{N}\sum_{n=1}^{N}(t_n^{action}-t_n^{observe})
\]

Generalization across scenarios is reported by evaluating the same checkpoint on unseen replay windows and computing per-scenario summary deltas.
