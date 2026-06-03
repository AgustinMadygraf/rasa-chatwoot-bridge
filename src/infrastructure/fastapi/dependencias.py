"""
Path: src/infrastructure/fastapi/dependencias.py
"""

from functools import lru_cache
from src.application.orquestador import Orquestador
from src.interface_adapters.controllers.controlador_webhook import ControladorWebhook
from src.interface_adapters.presenters.presentador_webhook import PresentadorWebhook
from src.infrastructure.httpx.puerta_enlace_chatwoot import HttpPuertaEnlaceChatwoot
from src.infrastructure.httpx.puerta_enlace_rasa import HttpPuertaEnlaceRasa
from src.infrastructure.settings.config import ajustes

@lru_cache()
def obtener_puerta_enlace_chatwoot() -> HttpPuertaEnlaceChatwoot:
    return HttpPuertaEnlaceChatwoot(
        base_url=ajustes.chatwoot_base_url,
        api_token=ajustes.chatwoot_api_token,
        account_id=ajustes.chatwoot_account_id
    )

@lru_cache()
def obtener_puerta_enlace_rasa() -> HttpPuertaEnlaceRasa:
    return HttpPuertaEnlaceRasa(rasa_url=ajustes.rasa_url)

@lru_cache()
def obtener_orquestador() -> Orquestador:
    return Orquestador(
        obtener_puerta_enlace_chatwoot(),
        obtener_puerta_enlace_rasa()
    )

@lru_cache()
def obtener_controlador_webhook() -> ControladorWebhook:
    presentador = PresentadorWebhook()
    return ControladorWebhook(obtener_orquestador(), presentador, ajustes.chatwoot_webhook_token)
