.PHONY: install dev test lint format run-backend run-frontend demo train evaluate export

install:
	python -m pip install -e .[test,rl]

run-backend:
	uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

run-frontend:
	cd frontend && npm install && npm run dev

dev:
	docker compose up --build

test:
	pytest -q

train:
	python -m rl.training.train_single_house --config experiments/configs/single_house.yaml

evaluate:
	python -m rl.evaluation.compare_agents --config experiments/configs/community.yaml

export:
	python -m rl.evaluation.export_results --input experiments/outputs/csv --output experiments/outputs/parquet

demo:
	python -m backend.app.main
