"""
Path: main.py
"""

import uvicorn
from src.infrastructure.settings.config import ajustes

if __name__ == "__main__":
    uvicorn.run("src.infrastructure.fastapi.app:app", host="127.0.0.1", port=ajustes.app_port, reload=True)
