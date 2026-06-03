"""
Path: src/domain/message.py
"""

from dataclasses import dataclass
from enum import Enum

class MessageType(Enum):
    INCOMING = "incoming"
    OUTGOING = "outgoing"

class SenderRole(Enum):
    USER = "user"
    BOT = "bot"
    SYSTEM = "system"

@dataclass(frozen=True)
class Message:
    conversation_id: str
    content: str
    sender_id: str
    sender_role: SenderRole
    message_type: MessageType
