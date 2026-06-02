"""
Path: src/infrastructure/web/fastapi/app.py
"""

from fastapi import FastAPI
from src.interface_adapters.controllers.controlador_webhook import router as webhook_router
from src.application.orquestador import Orquestador
from src.infrastructure.gateways.puerta_enlace_chatwoot import HttpPuertaEnlaceChatwoot
from src.infrastructure.gateways.puerta_enlace_rasa import HttpPuertaEnlaceRasa
from src.interface_adapters.controllers import controlador_webhook
from src.infrastructure.settings.config import ajustes
from src.infrastructure.settings.logger import logger

app: FastAPI = FastAPI()

# Inyección de dependencias simple usando configuración y logger
puerta_enlace_chatwoot = HttpPuertaEnlaceChatwoot(
    base_url=ajustes.chatwoot_base_url,
    api_token=ajustes.chatwoot_api_token,
    account_id=ajustes.chatwoot_account_id
)
puerta_enlace_rasa = HttpPuertaEnlaceRasa(rasa_url=ajustes.rasa_url)
orquestador = Orquestador(puerta_enlace_chatwoot, puerta_enlace_rasa)

logger.info("Orquestador inicializado correctamente.")

# Inyectar dependencia del orquestador para el webhook
async def obtener_orquestador():
    return orquestador

# Actualizar la dependencia del controlador dinámicamente
controlador_webhook.obtener_orquestador = obtener_orquestador

app.include_router(webhook_router)
