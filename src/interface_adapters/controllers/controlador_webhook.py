"""
Path: src/interface_adapters/controllers/controlador_webhook.py
"""

from typing import Any, Dict, Optional
from src.application.orquestador import Orquestador
from src.application.transformador import TransformadorChatwoot
from src.domain.message import Message

class ControladorWebhook:
    def __init__(self, orquestador: Orquestador, webhook_token: Optional[str] = None):
        self.orquestador = orquestador
        self.webhook_token = webhook_token

    async def manejar_webhook_chatwoot(self, payload: Dict[str, Any], token: Optional[str] = None) -> Dict[str, str]:
        # Validación del token de seguridad si está configurado
        if self.webhook_token:
            if token != self.webhook_token:
                return {"status": "error", "message": "Token de validación inválido"}

        mensaje: Message = TransformadorChatwoot.a_dominio(payload)
        await self.orquestador.manejar_mensaje_entrante(mensaje)
        return {"status": "ok"}
