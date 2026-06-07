# Path: src/aplicacion/puertos/puerta_enlace_chatwoot.py

from typing import Protocol
from src.dominio.mensaje import Mensaje

class PuertaEnlaceChatwoot(Protocol):
    async def enviar_mensaje(self, mensaje: Mensaje) -> None: ...
