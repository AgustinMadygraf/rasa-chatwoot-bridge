"""
Path: src/application/ports/servicio_tunel.py
"""

from typing import Protocol, Optional, Any

class ServicioTunel(Protocol):
    def iniciar(self, logger: Any) -> Optional[str]: ...
