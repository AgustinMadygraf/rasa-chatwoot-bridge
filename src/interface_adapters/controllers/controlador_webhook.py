"""
Path: src/interface_adapters/controllers/controlador_webhook.py
"""

from typing import Any, Dict, Optional
from src.application.orquestador import Orquestador
from src.application.transformador import TransformadorChatwoot
from src.application.exceptions import AccesoNoAutorizadoError, ErrorProcesamientoWebhook
from src.domain.message import Message
from src.interface_adapters.presenters.presentador_webhook import PresentadorWebhookInterface

class ControladorWebhook:
    def __init__(self, orquestador: Orquestador, presentador: PresentadorWebhookInterface, webhook_token: Optional[str] = None):
        self.orquestador = orquestador
        self.presentador = presentador
        self.webhook_token = webhook_token

    async def manejar_webhook_chatwoot(self, payload: Dict[str, Any], token: Optional[str] = None) -> Dict[str, Any]:
        # Validación estricta de seguridad
        if self.webhook_token:
            if token != self.webhook_token:
                raise AccesoNoAutorizadoError("Token de validación inválido")

        try:
            mensaje: Message = TransformadorChatwoot.a_dominio(payload)
            await self.orquestador.manejar_mensaje_entrante(mensaje)
            return self.presentador.respuesta_exitosa()
            
        except Exception as e:
            # Envolvemos el error en una excepción de la capa de aplicación
            raise ErrorProcesamientoWebhook(f"Error procesando webhook: {str(e)}")
