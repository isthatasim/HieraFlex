# Market Design

## Modes
- Fixed tariff
- Real-time tariff
- Local community market
- Hybrid local+grid mode

## Clearing
Current implementation:
1. House agents submit bids/offers from net demand/surplus.
2. Pairwise matching engine settles nonnegative flows \(q_{i,j,t}\).
3. Local clearing price uses midpoint of external buy/sell tariffs.
4. Residual unmet demand/surplus is settled with grid import/export.
5. Fairness term tracks inequality in accumulated savings.

## Fairness-aware extension
A proportional allocation can be applied to adjust accepted offers:
\[
q^{\star}_{i,j,t} = q_{i,j,t}\cdot w_h,\quad
w_h \propto \frac{1}{\epsilon + S_h}
\]
for lower-savings houses to receive higher flexibility priority.

## Trade metrics
- total local traded energy
- local trading revenue
- clearing-price trajectory
- fairness indicators (variance, Jain index)
