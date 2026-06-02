"""
Path: src/interface_adapters/gateways/puerta_enlace_chatwoot.py
"""

from abc import ABC, abstractmethod
from src.domain.entities.message import Message

class PuertaEnlaceChatwoot(ABC):
    @abstractmethod
    async def enviar_mensaje(self, conversation_id: str, message: Message) -> None:
        pass
