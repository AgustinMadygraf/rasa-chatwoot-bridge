"""
Path: src/infrastructure/fastapi/app.py
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.infrastructure.fastapi.rutas_webhook import router as webhook_router
from src.infrastructure.settings.logger import logger
from src.infrastructure.pyngrok.servicio_ngrok import iniciar_tunel

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Acciones al iniciar
    iniciar_tunel()
    logger.info("Aplicación iniciada y túnel configurado.")
    yield
    # Acciones al cerrar
    logger.info("Aplicación cerrándose.")

app: FastAPI = FastAPI(lifespan=lifespan)

# Incluir rutas - Las dependencias se resuelven automáticamente vía Depends
app.include_router(webhook_router)
