# Resource Visualization

HieraFlex renders hierarchical telemetry from community to appliance level.

## Drill-down path
Community -> House -> Resource -> Appliance

## Resource-level signals
- house total load
- flexible load and non-flexible load
- per-appliance power and operational state
- appliance start/defer events
- battery charge/discharge power and SOC
- EV charging power and SOC
- PV production/use/curtailment
- grid import/export
- local trade exchange
- price signal and agent action overlay

## API payloads
Primary resource endpoint:
- `GET /houses/{house_id}/resources?limit=N`

Returns:
- `timeline[]`: house total and price
- `appliances[]`: per-appliance traces and nominal ratings

## Frontend components
- `ResourceTimeline`: per-house load trace
- `PriceOverlayChart`: load + price alignment
- `ResourceLayer`: aggregate resource cards
- `ApplianceExplorer`: appliance state and context
- `ExplainabilityPanel`: action reason summary

## UX interactions
- trace toggles per resource signal
- zoomable time windows through replay selection
- baseline vs policy overlays
- action-event overlays on time series

## Data formatting rules
- monotonic timestamps per series
- explicit units (`kW`, `kWh`, `SOC`)
- sparse missing values treated as `null` and rendered gracefully
- bounded query limits for responsive rendering
