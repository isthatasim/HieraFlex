# Mathematical Model

## Community objective

\[
\min J_{\text{comm}} =
\sum_t \Big[
\pi_t^{\text{grid,buy}}\sum_h P_{h,t}^{\text{grid,in}} -
\pi_t^{\text{grid,sell}}\sum_h P_{h,t}^{\text{grid,out}} +
\lambda_{\text{peak}} P_t^{\text{peak,excess}} +
\lambda_{\text{fair}}\Phi_t^{\text{fair}}
\Big]
+
\sum_{h,t}\Big[
\lambda_{\text{comfort}} C_{h,t}^{\text{comfort}}+
\lambda_{\text{switch}} C_{h,t}^{\text{switch}}+
\lambda_{\text{deadline}} C_{h,t}^{\text{deadline}}
\Big]
\]

## House objective

\[
\min J_h = \sum_t \Big[
\pi_t^{\text{grid,buy}}P_{h,t}^{\text{grid,in}}-
\pi_t^{\text{grid,sell}}P_{h,t}^{\text{grid,out}}-
Rev_{h,t}^{\text{trade}}+
\lambda_{\text{peak}} C_{h,t}^{\text{peak}}+
\lambda_{\text{comfort}} C_{h,t}^{\text{comfort}}+
\lambda_{\text{switch}} C_{h,t}^{\text{switch}}+
\lambda_{\text{deadline}} C_{h,t}^{\text{deadline}}+
\lambda_{\text{violation}} C_{h,t}^{\text{violation}}
\Big]
\]

## Fairness

Implemented options:

1. Savings variance penalty:
\[
\Phi^{\text{fair}} = \sum_h (S_h - \bar S)^2
\]

2. Jain fairness index:
\[
J = \frac{(\sum_h S_h)^2}{|\mathcal{H}|\sum_h S_h^2}
\]

The runtime currently reports Jain-based fairness and keeps variance penalty available in market scoring.

## Baseline heuristics

Cheapest-slot heuristic starts when current price is under a rolling quantile threshold:
\[
a_t =
\begin{cases}
\text{start}, & \pi_t \le Q_q(\pi_{t-w+1:t}) \\
\text{defer}, & \pi_t > Q_q(\pi_{t-w+1:t}) \land \text{slack}>0 \\
\text{keep}, & \text{otherwise}
\end{cases}
\]
