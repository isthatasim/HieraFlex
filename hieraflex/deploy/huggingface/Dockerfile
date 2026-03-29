FROM node:20-alpine AS frontend-build

WORKDIR /workspace/hieraflex/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend ./
RUN npm run build -- --base /ui/

FROM python:3.11-slim

WORKDIR /workspace/hieraflex

COPY pyproject.toml README.md ./
COPY backend ./backend
COPY core ./core
COPY data ./data
COPY rl ./rl
COPY experiments ./experiments
COPY deploy/huggingface ./deploy/huggingface
COPY deploy/huggingface/hf_requirements.txt ./hf_requirements.txt
COPY --from=frontend-build /workspace/hieraflex/frontend/dist ./frontend/dist

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r hf_requirements.txt

EXPOSE 7860

ENV API_HOST=0.0.0.0
ENV API_PORT=7860
ENV HIERAFLEX_MODE=public-demo
ENV HIERAFLEX_SERVE_FRONTEND=1

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "7860"]
