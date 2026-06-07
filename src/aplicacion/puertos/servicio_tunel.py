"""
Puerto para el servicio de túnel (ej. ngrok).
"""

from typing import Protocol, Optional
from src.aplicacion.puertos.registrador import Registrador

class ServicioTunel(Protocol):
    def iniciar(self, logger: Registrador) -> Optional[str]: ...
