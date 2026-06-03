"""
Path: src/interface_adapters/presenters/presentador_rasa.py
"""

from typing import Any, Dict, Protocol
from src.domain.message import Message

class PresentadorRasaInterface(Protocol):
    def a_payload_rasa(self, message: Message) -> Dict[str, Any]: ...

class PresentadorRasa:
    def a_payload_rasa(self, message: Message) -> Dict[str, Any]:
        return {"sender": message.conversation_id, "message": message.content}
