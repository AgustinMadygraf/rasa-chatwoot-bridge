"""
Puerto para la comunicación con Rasa.
"""

from abc import ABC, abstractmethod
from typing import List
from src.dominio.mensaje import Mensaje

class PuertaEnlaceRasa(ABC):
    @abstractmethod
    async def enviar_a_rasa(self, mensaje: Mensaje) -> List[Mensaje]:
        pass
