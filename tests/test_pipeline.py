import unittest
from unittest.mock import MagicMock
from src.application.pipeline import MessagePipeline
from src.domain.message import Message, MessageType, SenderRole

class TestMessagePipeline(unittest.TestCase):
    def setUp(self):
        self.mock_logger = MagicMock()
        self.pipeline = MessagePipeline(self.mock_logger)

    def test_should_process_incoming_message(self):
        message = Message(
            conversation_id="123",
            content="hola",
            sender_id="user1",
            sender_role=SenderRole.USER,
            message_type=MessageType.INCOMING
        )
        self.assertTrue(self.pipeline.should_process(message))

    def test_should_not_process_outgoing_message(self):
        message = Message(
            conversation_id="123",
            content="respuesta",
            sender_id="bot",
            sender_role=SenderRole.BOT,
            message_type=MessageType.OUTGOING
        )
        self.assertFalse(self.pipeline.should_process(message))
        self.mock_logger.info.assert_called_once()
        self.assertIn("ignorado", self.mock_logger.info.call_args[0][0])

if __name__ == "__main__":
    unittest.main()
