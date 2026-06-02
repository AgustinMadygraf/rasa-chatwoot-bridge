from typing import Any, Dict, Optional
from src.application.orquestador import Orquestador
from src.application.transformador import TransformadorChatwoot
from src.domain.message import Message
from src.infrastructure.settings.config import ajustes

class ControladorWebhook:
    def __init__(self, orquestador: Orquestador):
        self.orquestador = orquestador

    async def manejar_webhook_chatwoot(self, payload: Dict[str, Any], token: Optional[str] = None) -> Dict[str, str]:
        # Validación del token de seguridad si está configurado
        if ajustes.chatwoot_webhook_token:
            if token != ajustes.chatwoot_webhook_token:
                return {"status": "error", "message": "Token de validación inválido"}

        mensaje: Message = TransformadorChatwoot.a_dominio(payload)
        await self.orquestador.manejar_mensaje_entrante(mensaje)
        return {"status": "ok"}
