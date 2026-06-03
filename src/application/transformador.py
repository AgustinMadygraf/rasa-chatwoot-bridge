"""
Path: src/application/transformador.py
"""

from typing import Any, Dict
from src.domain.message import Message, MessageType, SenderRole

class TransformadorChatwoot:
    @staticmethod
    def a_dominio(payload: Dict[str, Any]) -> Message:
        # Mapeo directo del tipo de mensaje de Chatwoot
        raw_type = payload.get("message_type", "incoming")
        msg_type = MessageType.OUTGOING if raw_type == "outgoing" else MessageType.INCOMING
        
        # Mapeo del rol (usamos outgoing para identificar el bot)
        sender_id = str(payload["sender"]["id"])
        
        # Si es outgoing, forzamos rol BOT para asegurar consistencia
        role = SenderRole.BOT if msg_type == MessageType.OUTGOING else SenderRole.USER
        
        return Message(
            conversation_id=str(payload["conversation"]["id"]),
            content=payload.get("content") or "",
            sender_id=sender_id,
            sender_role=role,
            message_type=msg_type
        )
