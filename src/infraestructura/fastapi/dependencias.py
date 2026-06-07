# Path: src/infraestructura/fastapi/dependencias.py

from functools import lru_cache
from typing import Optional
from src.aplicacion.casos_de_uso.procesar_mensaje_entrante import ProcesarMensajeEntrante
from src.adaptadores.controladores.controlador_webhook import ControladorWebhook
from src.adaptadores.presentadores.presentador_webhook import PresentadorWebhook
from src.adaptadores.presentadores.presentador_chatwoot import PresentadorChatwoot
from src.adaptadores.presentadores.presentador_rasa import PresentadorRasa
from src.infraestructura.httpx.cliente_httpx import ClienteHttpx
from src.adaptadores.pasarelas.pasarela_chatwoot import PasarelaChatwoot
from src.adaptadores.pasarelas.pasarela_rasa import PasarelaRasa
from src.infraestructura.pyngrok.ngrok_gateway import PasarelaNgrok
from src.infraestructura.settings.config import ajustes
from src.infraestructura.settings.registrador import logger

@lru_cache()
def obtener_cliente_http() -> ClienteHttpx:
    return ClienteHttpx()

@lru_cache()
def obtener_servicio_tunel() -> Optional[PasarelaNgrok]:
    if ajustes.usar_ngrok:
        return PasarelaNgrok()
    return None

@lru_cache()
def obtener_puerta_enlace_chatwoot() -> PasarelaChatwoot:
    return PasarelaChatwoot(
        obtener_cliente_http(),
        PresentadorChatwoot(),
        base_url=ajustes.url_base_chatwoot,
        api_token=ajustes.token_api_chatwoot,
        account_id=ajustes.id_cuenta_chatwoot
    )

@lru_cache()
def obtener_puerta_enlace_rasa() -> PasarelaRasa:
    return PasarelaRasa(
        obtener_cliente_http(),
        PresentadorRasa(),
        rasa_url=ajustes.url_rasa
    )

@lru_cache()
def obtener_caso_de_uso_procesar_mensaje() -> ProcesarMensajeEntrante:
    return ProcesarMensajeEntrante(
        puerta_enlace_chatwoot=obtener_puerta_enlace_chatwoot(),
        puerta_enlace_rasa=obtener_puerta_enlace_rasa(),
        usar_rasa=ajustes.usar_rasa,
        logger=logger
    )

@lru_cache()
def obtener_controlador_webhook() -> ControladorWebhook:
    presentador = PresentadorWebhook()
    return ControladorWebhook(obtener_caso_de_uso_procesar_mensaje(), presentador, None)
