"""
Path: src/interface_adapters/presenters/presentador_rasa.py
"""

from typing import Any, Dict, Protocol
from src.dominio.mensaje import Mensaje

class PresentadorRasaInterface(Protocol):
    def a_payload_rasa(self, message: Mensaje) -> Dict[str, Any]: ...

class PresentadorRasa:
    def a_payload_rasa(self, message: Mensaje) -> Dict[str, Any]:
        return {"sender": message.id_conversacion.valor, "message": message.contenido}
