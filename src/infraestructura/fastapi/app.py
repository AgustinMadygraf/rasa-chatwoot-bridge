from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.infraestructura.fastapi.rutas_webhook import router as webhook_router
from src.infraestructura.settings.registrador import logger
from src.infraestructura.fastapi.dependencias import obtener_servicio_tunel

@asynccontextmanager
async def lifespan(app: FastAPI):
    servicio_tunel = obtener_servicio_tunel()
    if servicio_tunel:
        servicio_tunel.iniciar(logger)
    logger.informar('Aplicación iniciada.')
    yield
    if servicio_tunel:
        servicio_tunel.cerrar()
    logger.informar('Aplicación cerrándose.')

app: FastAPI = FastAPI(lifespan=lifespan)

app.include_router(webhook_router)
