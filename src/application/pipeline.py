"""
Path: src/application/pipeline.py
"""

from src.domain.message import Message, MessageType
from src.application.ports.logger import Logger

class MessagePipeline:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.filters = [self.filter_outgoing_messages]

    def filter_outgoing_messages(self, message: Message) -> bool:
        if message.message_type == MessageType.OUTGOING:
            self.logger.info(f"Filtro Pipeline: Mensaje OUTGOING (id={message.conversation_id}) ignorado.")
            return False
        return True

    def should_process(self, message: Message) -> bool:
        return all(f(message) for f in self.filters)
