"""
Puerto para la comunicación con Chatwoot.
"""

from abc import ABC, abstractmethod
from src.dominio.mensaje import Mensaje

class PuertaEnlaceChatwoot(ABC):
    @abstractmethod
    async def enviar_mensaje(self, id_conversacion: str, mensaje: Mensaje) -> None:
        pass
