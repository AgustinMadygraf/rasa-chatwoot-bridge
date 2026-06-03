import unittest
from unittest.mock import MagicMock, AsyncMock
from src.application.orquestador import Orquestador
from src.domain.message import Message, MessageType, SenderRole

class TestOrquestador(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.mock_chatwoot = AsyncMock()
        self.mock_rasa = AsyncMock()
        self.mock_logger = MagicMock()
        self.orquestador = Orquestador(
            self.mock_chatwoot,
            self.mock_rasa,
            use_rasa=True,
            logger=self.mock_logger
        )

    async def test_manejar_mensaje_entrante_con_rasa(self):
        mensaje = Message(
            conversation_id="123",
            content="hola",
            sender_id="user1",
            sender_role=SenderRole.USER,
            message_type=MessageType.INCOMING
        )
        
        respuesta_rasa = Message(
            conversation_id="123",
            content="hola soy rasa",
            sender_id="bot",
            sender_role=SenderRole.BOT,
            message_type=MessageType.OUTGOING
        )
        self.mock_rasa.enviar_a_rasa.return_value = [respuesta_rasa]

        await self.orquestador.manejar_mensaje_entrante(mensaje)

        self.mock_rasa.enviar_a_rasa.assert_called_once_with(mensaje)
        self.mock_chatwoot.enviar_mensaje.assert_called_once()
        self.mock_logger.info.assert_any_call("Orquestador procesando mensaje. Modo Rasa: True")

if __name__ == "__main__":
    unittest.main()
