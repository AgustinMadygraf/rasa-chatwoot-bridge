# Path: src/adaptadores/controladores/controlador_webhook.py

from typing import Any, Dict, Optional
from src.aplicacion.casos_de_uso.procesar_mensaje_entrante import ProcesarMensajeEntrante
from src.aplicacion.excepciones import AccesoNoAutorizadoError, ErrorProcesamientoWebhook
from src.adaptadores.controladores.mapeador_webhook import MapeadorMensajeWebhook
from src.adaptadores.presentadores.presentador_webhook import PresentadorWebhookInterface

class ControladorWebhook:
    def __init__(self, caso_de_uso: ProcesarMensajeEntrante, presentador: PresentadorWebhookInterface, webhook_token: Optional[str] = None):
        self.caso_de_uso = caso_de_uso
        self.presentador = presentador
        self.webhook_token = webhook_token

    async def manejar_webhook_chatwoot(self, payload: Dict[str, Any], token: Optional[str] = None) -> Dict[str, Any]:
        if self.webhook_token and token != self.webhook_token:
            raise AccesoNoAutorizadoError("Token de validación inválido")

        try:
            mensaje = MapeadorMensajeWebhook.desde_payload_chatwoot(payload)
            await self.caso_de_uso.ejecutar(mensaje)
            return self.presentador.respuesta_exitosa()
        except ErrorProcesamientoWebhook:
            raise
        except Exception as e:
            raise ErrorProcesamientoWebhook(f"Error procesando webhook: {str(e)}")
