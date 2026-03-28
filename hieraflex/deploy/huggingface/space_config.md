# Space Runtime Config

## Recommended hardware
- CPU basic for demo replay
- T4 small for remote inference benchmark mode

## Commands
- Health: `GET /`
- Start replay: `POST /simulation/start`
- Listen live channels: `/ws/community`, `/ws/houses`, `/ws/actions`, `/ws/trades`, `/ws/price`

## Notes
Hard control loops remain local backend logic. Hugging Face is used for artifact hosting and demo delivery.
