"""
Path: src/infrastructure/fastapi/rutas_webhook.py
"""

from typing import Any, Dict
from src.application.orquestador import Orquestador
from src.application.transformador import TransformadorChatwoot
from src.domain.entities.message import Message

class ControladorWebhook:
    def __init__(self, orquestador: Orquestador):
        self.orquestador = orquestador

    async def manejar_webhook_chatwoot(self, payload: Dict[str, Any]) -> Dict[str, str]:
        mensaje: Message = TransformadorChatwoot.a_dominio(payload)
        await self.orquestador.manejar_mensaje_entrante(mensaje)
        return {"status": "ok"}
