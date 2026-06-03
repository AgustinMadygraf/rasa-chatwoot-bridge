"""
Path: src/interface_adapters/presenters/presentador_rasa.py
"""

from typing import Any, Dict
from src.domain.message import Message

class PresentadorRasa:
    @staticmethod
    def a_payload_rasa(message: Message) -> Dict[str, Any]:
        return {"sender": message.conversation_id, "message": message.content}
