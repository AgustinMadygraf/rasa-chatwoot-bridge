# Path: src/aplicacion/puertos/servicio_tunel.py

from typing import Protocol, Optional
from src.aplicacion.puertos.registrador import Registrador

class ServicioTunel(Protocol):
    def iniciar(self, logger: Registrador) -> Optional[str]: ...
