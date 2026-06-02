"""
Path: src/domain/entities/message.py
"""

from dataclasses import dataclass
from enum import Enum

class MessageType(Enum):
    INCOMING = "incoming"
    OUTGOING = "outgoing"

@dataclass(frozen=True)
class Message:
    conversation_id: str
    content: str
    sender_id: str
    message_type: MessageType
