# Notation

## Sets and indices
- \(h \in \mathcal{H}\): houses
- \(a \in \mathcal{A}_h\): appliances/resources of house \(h\)
- \(t \in \mathcal{T}\): time steps
- \(k \in \mathcal{K}_h\): DER units (battery/EV/PV)
- \(i,j \in \mathcal{H}\): local trade participants
- \(\Delta t\): step duration

Optional:
- \(\mathcal{F}_h \subseteq \mathcal{A}_h\): flexible appliances
- \(\mathcal{N}_h \subseteq \mathcal{A}_h\): non-flexible appliances
- \(s \in \mathcal{S}\): scenarios
- \(e \in \mathcal{E}\): replay events

## Key parameters
- \(\bar P_{h,a}\): appliance nominal power
- \(d_{h,a}\): cycle duration
- \(t^{\text{earliest}}_{h,a}, t^{\text{latest}}_{h,a}\): scheduling window
- \(\omega_{h,a}\): priority weight
- \(\rho_{h,a}\): interruptibility flag
- \(\gamma_{h,a}\): discomfort weight

Price/market:
- \(\pi_t^{\text{grid,buy}}\), \(\pi_t^{\text{grid,sell}}\), \(\pi_t^{\text{local}}\), \(\pi_t^{\text{inc}}\)

Penalties/rewards:
- \(\lambda_{\text{peak}}, \lambda_{\text{comfort}}, \lambda_{\text{switch}}, \lambda_{\text{deadline}}, \lambda_{\text{violation}}, \lambda_{\text{fair}}, \lambda_{\text{resp}}, \lambda_{\text{trade}}, \lambda_{\text{self}}\)

All reward coefficients \(\alpha_1,\dots,\alpha_{10}\) are configurable in `experiments/configs/reward_weights.yaml`.
