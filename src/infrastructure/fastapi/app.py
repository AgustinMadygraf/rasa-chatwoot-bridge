"""
Path: src/infrastructure/fastapi/app.py
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.infrastructure.fastapi.rutas_webhook import router as webhook_router
from src.application.orquestador import Orquestador
from src.interface_adapters.controllers.controlador_webhook import ControladorWebhook
from src.infrastructure.httpx.puerta_enlace_chatwoot import HttpPuertaEnlaceChatwoot
from src.infrastructure.httpx.puerta_enlace_rasa import HttpPuertaEnlaceRasa
from src.infrastructure.fastapi import rutas_webhook
from src.infrastructure.settings.config import ajustes
from src.infrastructure.settings.logger import logger
from src.infrastructure.pyngrok.servicio_ngrok import iniciar_tunel

@asynccontextmanager
async def lifespan(app: FastAPI):
    iniciar_tunel()
    yield

app: FastAPI = FastAPI(lifespan=lifespan)

puerta_enlace_chatwoot = HttpPuertaEnlaceChatwoot(
    base_url=ajustes.chatwoot_base_url,
    api_token=ajustes.chatwoot_api_token,
    account_id=ajustes.chatwoot_account_id
)
puerta_enlace_rasa = HttpPuertaEnlaceRasa(rasa_url=ajustes.rasa_url)
orquestador = Orquestador(puerta_enlace_chatwoot, puerta_enlace_rasa)
controlador = ControladorWebhook(orquestador)

logger.info("Orquestador y Controlador inicializados correctamente.")

async def obtener_controlador_inyectado():
    return controlador

rutas_webhook.obtener_controlador = obtener_controlador_inyectado

app.include_router(webhook_router)
