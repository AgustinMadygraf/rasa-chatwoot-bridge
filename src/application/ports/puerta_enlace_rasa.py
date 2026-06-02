"""
Path: src/interface_adapters/gateways/puerta_enlace_rasa.py
"""

from abc import ABC, abstractmethod
from typing import List
from src.domain.message import Message

class PuertaEnlaceRasa(ABC):
    @abstractmethod
    async def enviar_a_rasa(self, message: Message) -> List[Message]:
        pass
