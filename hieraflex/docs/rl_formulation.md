# RL Formulation

HieraFlex models each house as an MDP agent in a multi-agent environment.

## State
For house \(h\) at time \(t\):
\[
s_{h,t} = [
\text{time}, \text{hour}, \text{day}, \pi_t, \pi_{t-w:t}, \hat\pi_{t:t+H},
\text{load}, \text{rolling load}, \text{appliance states}, \text{remaining cycles},
\text{deadline slack}, \text{action history}, \text{community load}, \text{trade signal},
\text{DER states}, \text{comfort indicators}
]
\]

## Action
Discrete action set includes:
- start appliance
- defer appliance
- keep
- battery charge/discharge
- EV charge bucket
- place bid
- place offer
- no-op

Continuous extensions (optional): dispatch rate, trade amount, priority weight.

## Transition
\[
\mathcal{P}(s_{t+1}|s_t,a_t)
\]
induced by replay trace dynamics, controller feasibility, local market clearing, and community coordination.

## Reward
\[
r_{h,t} =
-\alpha_1 C_{h,t}^{\text{energy}}
-\alpha_2 C_{h,t}^{\text{peak}}
-\alpha_3 C_{h,t}^{\text{comfort}}
-\alpha_4 C_{h,t}^{\text{switch}}
-\alpha_5 C_{h,t}^{\text{deadline}}
-\alpha_6 C_{h,t}^{\text{violation}}
+\alpha_7 Rev_{h,t}^{\text{trade}}
+\alpha_8 R_{h,t}^{\text{self}}
+\alpha_9 R_{h,t}^{\text{flex}}
+\alpha_{10} R_{h,t}^{\text{resp}}
\]

with \(\gamma\in(0,1)\) discount factor.

## Baselines implemented
1. Historical no-control (`FixedScheduleAgent`)
2. Rule-based price scheduler (`RuleBasedAgent`)
3. Cheapest-slot heuristic (`CheapestSlotAgent`)
4. PPO-based controller (`PPOAgent`)

## Metrics formulations
- \(\text{PAR}=\max_t P_t^{\text{comm}} / (\frac{1}{|\mathcal{T}|}\sum_t P_t^{\text{comm}})\)
- \(\text{Savings}_h = \text{Cost}_h^{\text{baseline}} - \text{Cost}_h^{\text{policy}}\)
- \(\text{SelfConsumption}_h = E_h^{\text{PV,local}} / E_h^{\text{PV,total}}\)
- price-response efficiency: benefit/correlation between high-price intervals and downward flexible demand response.
