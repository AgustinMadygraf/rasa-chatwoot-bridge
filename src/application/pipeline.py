"""
Path: src/application/pipeline.py
"""

from src.domain.message import Message, MessageType
from src.infrastructure.settings.logger import logger

class MessagePipeline:
    def __init__(self):
        self.filters = [self.filter_outgoing_messages]

    def filter_outgoing_messages(self, message: Message) -> bool:
        if message.message_type == MessageType.OUTGOING:
            logger.info(f"Filtro Pipeline: Mensaje OUTGOING (id={message.conversation_id}) ignorado.")
            return False
        return True

    def should_process(self, message: Message) -> bool:
        return all(f(message) for f in self.filters)
