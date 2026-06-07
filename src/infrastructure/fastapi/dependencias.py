"""
Path: src/infrastructure/fastapi/dependencias.py
"""

from functools import lru_cache
from typing import Optional
from src.application.orquestador import Orquestador
from src.application.tuberia import TuberiaMensajes
from src.interface_adapters.controllers.controlador_webhook import ControladorWebhook
from src.interface_adapters.presenters.presentador_webhook import PresentadorWebhook
from src.interface_adapters.presenters.presentador_chatwoot import PresentadorChatwoot
from src.interface_adapters.presenters.presentador_rasa import PresentadorRasa
from src.infrastructure.httpx.cliente_httpx import HttpxClient
from src.interface_adapters.gateways.gateway_chatwoot import GatewayChatwoot
from src.interface_adapters.gateways.gateway_rasa import GatewayRasa
from src.infrastructure.pyngrok.ngrok_gateway import NgrokGateway
from src.infrastructure.settings.config import ajustes
from src.infrastructure.settings.logger import logger

@lru_cache()
def obtener_http_client() -> HttpxClient:
    return HttpxClient()

@lru_cache()
def obtener_servicio_tunel() -> Optional[NgrokGateway]:
    if ajustes.usar_ngrok:
        return NgrokGateway()
    return None

@lru_cache()
def obtener_puerta_enlace_chatwoot() -> GatewayChatwoot:
    return GatewayChatwoot(
        obtener_http_client(),
        PresentadorChatwoot(),
        base_url=ajustes.chatwoot_base_url,
        api_token=ajustes.chatwoot_api_token,
        account_id=ajustes.chatwoot_account_id
    )

@lru_cache()
def obtener_puerta_enlace_rasa() -> GatewayRasa:
    return GatewayRasa(
        obtener_http_client(),
        PresentadorRasa(),
        rasa_url=ajustes.rasa_url
    )

@lru_cache()
def obtener_orquestador() -> Orquestador:
    return Orquestador(
        obtener_puerta_enlace_chatwoot(),
        obtener_puerta_enlace_rasa(),
        use_rasa=ajustes.use_rasa,
        logger=logger,
        tuberia=TuberiaMensajes(logger=logger)
    )

@lru_cache()
def obtener_controlador_webhook() -> ControladorWebhook:
    presentador = PresentadorWebhook()
    return ControladorWebhook(obtener_orquestador(), presentador, None)
