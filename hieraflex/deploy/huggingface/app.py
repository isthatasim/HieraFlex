from __future__ import annotations

import os

import uvicorn

from backend.app.main import app


if __name__ == "__main__":
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "7860"))
    uvicorn.run(app, host=host, port=port)
