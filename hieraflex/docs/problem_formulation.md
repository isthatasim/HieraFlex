# Problem Formulation

HieraFlex solves hierarchical multi-agent community energy coordination over replay horizon \(\mathcal{T}\).

## Decision variables
- \(x_{h,a,t} \in \{0,1\}\): appliance on/off
- \(y_{h,a,t} \in \{0,1\}\): start indicator
- \(z_{h,a,t} \in \{0,1\}\): defer/shift indicator
- \(P_{h,t}^{\text{grid,in}}, P_{h,t}^{\text{grid,out}} \ge 0\)
- \(q_{i,j,t} \ge 0\): local trade energy from \(i\) to \(j\)
- \(b_{h,t}, o_{h,t} \ge 0\): bids/offers
- optional DER variables for battery/EV/PV

## Household balance
For each \(h,t\):

\[
P_{h,t}^{\text{grid,in}} + P_{h,t}^{\text{pv,use}} + P_{h,t}^{\text{bat,dis}} + \sum_{j\ne h} q_{j,h,t}
=
P_{h,t}^{\text{base}} + \sum_{a\in\mathcal{A}_h} \bar P_{h,a} x_{h,a,t} + P_{h,t}^{\text{bat,ch}} + P_{h,t}^{\text{ev}} + \sum_{j\ne h} q_{h,j,t} + P_{h,t}^{\text{grid,out}}
\]

## Appliance constraints
1. Start at most once (or exactly once for mandatory):
\[
\sum_t y_{h,a,t} \le 1
\]

2. Start only in feasible window:
\[
y_{h,a,t}=0,\; t\notin[t^{\text{earliest}}_{h,a},\; t^{\text{latest}}_{h,a}-d_{h,a}+1]
\]

3. Non-interruptible cycle integrity:
\[
x_{h,a,t}=\sum_{\tau=\max(1,t-d_{h,a}+1)}^t y_{h,a,\tau},\quad \rho_{h,a}=0
\]

4. Deadline completion before \(t^{\text{latest}}_{h,a}\).

## Battery (optional)
\[
SOC_{h,t}^{\text{bat}}=SOC_{h,t-1}^{\text{bat}}+\eta_{h}^{\text{bat,ch}}P_{h,t}^{\text{bat,ch}}\Delta t-\frac{P_{h,t}^{\text{bat,dis}}\Delta t}{\eta_{h}^{\text{bat,dis}}}
\]

\[
SOC_h^{\min} \le SOC_{h,t}^{\text{bat}} \le SOC_h^{\max}
\]

\[
0\le P_{h,t}^{\text{bat,ch}}\le \bar P_h^{\text{bat,ch}}u_{h,t}^{\text{bat,ch}},\;0\le P_{h,t}^{\text{bat,dis}}\le \bar P_h^{\text{bat,dis}}u_{h,t}^{\text{bat,dis}}
\]

\[
u_{h,t}^{\text{bat,ch}}+u_{h,t}^{\text{bat,dis}}\le1
\]

## EV (optional)
\[
SOC_{h,t}^{\text{ev}}=SOC_{h,t-1}^{\text{ev}}+\eta_h^{\text{ev}}P_{h,t}^{\text{ev}}\Delta t
\]

\[
0\le P_{h,t}^{\text{ev}}\le \bar P_h^{\text{ev}},\quad P_{h,t}^{\text{ev}}=0\;\text{outside}\;[t_h^{\text{arrive}},t_h^{\text{depart}}]
\]

\[
SOC_{h,t_h^{\text{depart}}}^{\text{ev}}\ge SOC_h^{\text{ev,target}}
\]

## PV (optional)
\[
0 \le P_{h,t}^{\text{pv,use}} + P_{h,t}^{\text{pv,curt}} \le \bar P_{h,t}^{\text{pv,avail}}
\]

## Community limits
\[
P_t^{\text{comm}}=\sum_h P_{h,t}^{\text{total}},\quad P_t^{\text{comm}}\le P_{\text{cap}}^{\text{comm}}+P_t^{\text{peak,excess}},\;P_t^{\text{peak,excess}}\ge0
\]

## Trading constraints
\[
q_{i,j,t}\ge0,\quad q_{h,h,t}=0
\]
\[
\sum_{j\ne h} q_{h,j,t}\le o_{h,t},\quad \sum_{i\ne h} q_{i,h,t}\le b_{h,t}
\]

Local clearing is implemented as a centralized fairness-aware matching engine with residual settlement against grid tariffs.
