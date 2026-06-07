# Path: src/aplicacion/puertos/puerta_enlace_rasa.py

from typing import Protocol, List
from src.dominio.mensaje import Mensaje

class PuertaEnlaceRasa(Protocol):
    async def enviar_a_rasa(self, mensaje: Mensaje) -> List[Mensaje]: ...
