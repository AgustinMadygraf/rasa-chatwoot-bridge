"""
Puerto para la comunicación con Chatwoot.
"""

from typing import Protocol
from src.dominio.mensaje import Mensaje

class PuertaEnlaceChatwoot(Protocol):
    async def enviar_mensaje(self, mensaje: Mensaje) -> None: ...
