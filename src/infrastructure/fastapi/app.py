"""
Path: src/infrastructure/fastapi/rutas_webhook.py
"""

from fastapi import FastAPI
from src.infrastructure.fastapi.rutas_webhook import router as webhook_router
from src.application.orquestador import Orquestador
from src.interface_adapters.controllers.controlador_webhook import ControladorWebhook
from infrastructure.httpx.puerta_enlace_chatwoot import HttpPuertaEnlaceChatwoot
from infrastructure.httpx.puerta_enlace_rasa import HttpPuertaEnlaceRasa
from src.infrastructure.fastapi import rutas_webhook
from src.infrastructure.settings.config import ajustes
from src.infrastructure.settings.logger import logger

app: FastAPI = FastAPI()

# Inicialización de dependencias
puerta_enlace_chatwoot = HttpPuertaEnlaceChatwoot(
    base_url=ajustes.chatwoot_base_url,
    api_token=ajustes.chatwoot_api_token,
    account_id=ajustes.chatwoot_account_id
)
puerta_enlace_rasa = HttpPuertaEnlaceRasa(rasa_url=ajustes.rasa_url)
orquestador = Orquestador(puerta_enlace_chatwoot, puerta_enlace_rasa)
controlador = ControladorWebhook(orquestador)

logger.info("Orquestador y Controlador inicializados correctamente.")

# Inyectar dependencia del controlador
async def obtener_controlador_inyectado():
    return controlador

# Actualizar la dependencia en el módulo de rutas
rutas_webhook.obtener_controlador = obtener_controlador_inyectado

app.include_router(webhook_router)
