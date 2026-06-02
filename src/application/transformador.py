"""
Path: src/application/transformador.py
"""

from typing import Any, Dict
from src.domain.entities.message import Message, MessageType

class TransformadorChatwoot:
    @staticmethod
    def a_dominio(payload: Dict[str, Any]) -> Message:
        return Message(
            conversation_id=str(payload["conversation"]["id"]),
            content=payload["content"],
            sender_id=str(payload["sender"]["id"]),
            message_type=MessageType.INCOMING
        )
