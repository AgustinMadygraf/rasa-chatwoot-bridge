"""
Path: src/interface_adapters/presenters/presentador_chatwoot.py
"""

from typing import Any, Dict, Protocol
from src.dominio.mensaje import Mensaje

class PresentadorChatwootInterface(Protocol):
    def a_payload_chatwoot(self, message: Mensaje) -> Dict[str, Any]: ...

class PresentadorChatwoot:
    def a_payload_chatwoot(self, message: Mensaje) -> Dict[str, Any]:
        return {"content": message.contenido, "message_type": "outgoing"}
