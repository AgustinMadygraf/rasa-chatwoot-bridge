"""
Path: src/interface_adapters/presenters/presentador_chatwoot.py
"""

from typing import Any, Dict
from src.domain.message import Message

class PresentadorChatwoot:
    @staticmethod
    def a_payload_chatwoot(message: Message) -> Dict[str, Any]:
        return {"content": message.content, "message_type": "outgoing"}
