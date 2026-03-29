# Problem Formulation

HieraFlex solves a hierarchical, replay-driven, price-responsive control problem over a discrete horizon \(t \in \mathcal{T}\), houses \(h \in \mathcal{H}\), appliances \(a \in \mathcal{A}_h\), and optional DER resources \(k \in \mathcal{K}_h\).

## Core sets and indices
- \(h \in \mathcal{H}\): houses
- \(a \in \mathcal{A}_h\): appliances/resources for house \(h\)
- \(f \in \mathcal{F}_h \subseteq \mathcal{A}_h\): flexible appliances
- \(n \in \mathcal{N}_h \subseteq \mathcal{A}_h\): non-flexible appliances
- \(i,j \in \mathcal{H}\): local trading pair indices
- \(t \in \mathcal{T}\): replay/training time index
- \(\Delta t\): step duration

## Main decision variables
- \(x_{h,a,t} \in \{0,1\}\): appliance on/off
- \(y_{h,a,t} \in \{0,1\}\): appliance start
- \(P_{h,t}^{grid,in}, P_{h,t}^{grid,out} \ge 0\): grid import/export
- \(q_{i,j,t} \ge 0\): local trade from house \(i\) to \(j\)
- \(P_{h,t}^{bat,ch}, P_{h,t}^{bat,dis}, SOC_{h,t}^{bat}\): battery variables (optional)
- \(P_{h,t}^{ev}, SOC_{h,t}^{ev}\): EV charging variables (optional)
- \(P_{h,t}^{pv,use}, P_{h,t}^{pv,curt}\): PV use/curtailment (optional)

## House-level balance
For every \(h,t\):

\[
P_{h,t}^{grid,in}
+ P_{h,t}^{pv,use}
+ P_{h,t}^{bat,dis}
+ \sum_{j \ne h} q_{j,h,t}
=
P_{h,t}^{base}
+ \sum_{a \in \mathcal{A}_h}\bar P_{h,a}x_{h,a,t}
+ P_{h,t}^{bat,ch}
+ P_{h,t}^{ev}
+ \sum_{j \ne h} q_{h,j,t}
+ P_{h,t}^{grid,out}
\]

## Appliance feasibility
1. Start once (or exactly once for mandatory tasks):
\[
\sum_t y_{h,a,t} \le 1
\]
2. Window compliance:
\[
y_{h,a,t}=0 \quad \forall t \notin [t_{h,a}^{earliest}, t_{h,a}^{latest}-d_{h,a}+1]
\]
3. Non-interruptible continuity (\(\rho_{h,a}=0\)):
\[
x_{h,a,t}=\sum_{\tau=\max(1,t-d_{h,a}+1)}^t y_{h,a,\tau}
\]
4. Completion before latest finish.

## Resource dynamics
Battery:
\[
SOC_{h,t}^{bat}=SOC_{h,t-1}^{bat}+\eta_h^{bat,ch}P_{h,t}^{bat,ch}\Delta t-\frac{P_{h,t}^{bat,dis}\Delta t}{\eta_h^{bat,dis}}
\]
\[
SOC_h^{min} \le SOC_{h,t}^{bat} \le SOC_h^{max}
\]

EV:
\[
SOC_{h,t}^{ev}=SOC_{h,t-1}^{ev}+\eta_h^{ev}P_{h,t}^{ev}\Delta t
\]
\[
P_{h,t}^{ev}=0 \quad \forall t \notin [t_h^{arrive}, t_h^{depart}], \quad SOC_{h,t_h^{depart}}^{ev}\ge SOC_h^{ev,target}
\]

PV:
\[
0 \le P_{h,t}^{pv,use}+P_{h,t}^{pv,curt} \le \bar P_{h,t}^{pv,avail}
\]

## Community coupling and trading
\[
P_t^{comm}=\sum_h P_{h,t}^{total}, \quad P_t^{comm}\le P_{cap}^{comm}+P_t^{peak,excess}, \quad P_t^{peak,excess}\ge 0
\]
\[
q_{i,j,t}\ge 0,\quad q_{h,h,t}=0,\quad \sum_{j\ne h}q_{h,j,t}\le o_{h,t},\quad \sum_{i\ne h}q_{i,h,t}\le b_{h,t}
\]

HieraFlex uses centralized local clearing with fairness-aware proportional allocation and residual settlement against external grid tariffs.

## Online control loop
At each replay step, every house executes:
1. Observe local/resource/community state.
2. Reason over price, slack, comfort, and trade opportunity.
3. Plan a short-horizon feasible action.
4. Act through appliance/resource controllers.
5. Reflect and log reward decomposition, violations, and explanation.

## Long-horizon training/evaluation split
Episodes are sampled from replay windows:
- train windows \(\mathcal{T}_{train}\)
- validation windows \(\mathcal{T}_{val}\)
- test windows \(\mathcal{T}_{test}\)

Best checkpoint is selected by a configurable criterion (default highest episodic return on evaluation windows), with deterministic evaluation mode and fixed seeds.
