"""
Path: src/interface_adapters/presenters/presentador_chatwoot.py
"""

from typing import Any, Dict, Protocol
from src.domain.message import Message

class PresentadorChatwootInterface(Protocol):
    def a_payload_chatwoot(self, message: Message) -> Dict[str, Any]: ...

class PresentadorChatwoot:
    def a_payload_chatwoot(self, message: Message) -> Dict[str, Any]:
        return {"content": message.content, "message_type": "outgoing"}
