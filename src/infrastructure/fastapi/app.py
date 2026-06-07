from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.infrastructure.fastapi.rutas_webhook import router as webhook_router
from src.infrastructure.settings.logger import logger
from src.infrastructure.fastapi.dependencias import obtener_servicio_tunel

@asynccontextmanager
async def lifespan(app: FastAPI):
    servicio_tunel = obtener_servicio_tunel()
    if servicio_tunel:
        servicio_tunel.iniciar(logger)
    logger.info("Aplicación iniciada.")
    yield
    # --- MEJORA: Cerrar túnel al apagar ---
    if servicio_tunel:
        servicio_tunel.cerrar()
    logger.info("Aplicación cerrándose.")

app: FastAPI = FastAPI(lifespan=lifespan)

app.include_router(webhook_router)
