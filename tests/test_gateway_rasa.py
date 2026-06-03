import unittest
from unittest.mock import AsyncMock, MagicMock
from src.interface_adapters.gateways.gateway_rasa import GatewayRasa
from src.domain.message import Message, MessageType, SenderRole

class TestGatewayRasa(unittest.IsolatedAsyncioTestCase):
    async def test_enviar_a_rasa_exito(self):
        mock_http_client = AsyncMock()
        mock_presentador = MagicMock()
        
        mock_presentador.a_payload_rasa.return_value = {"sender": "123", "message": "hola"}
        
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"recipient_id": "123", "text": "¡Hola! ¿En qué puedo ayudarte?"}
        ]
        mock_http_client.post.return_value = mock_response
        
        gateway = GatewayRasa(
            http_client=mock_http_client,
            presentador=mock_presentador,
            rasa_url="http://localhost:5005"
        )
        
        mensaje_original = Message(
            conversation_id="123",
            content="hola",
            sender_id="user1",
            sender_role=SenderRole.USER,
            message_type=MessageType.INCOMING
        )
        
        resultado = await gateway.enviar_a_rasa(mensaje_original)
        
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].conversation_id, "123")
        self.assertEqual(resultado[0].content, "¡Hola! ¿En qué puedo ayudarte?")
        self.assertEqual(resultado[0].sender_id, "bot")
        self.assertEqual(resultado[0].sender_role, SenderRole.BOT)
        self.assertEqual(resultado[0].message_type, MessageType.OUTGOING)
        
        mock_http_client.post.assert_called_once_with(
            "http://localhost:5005/webhooks/rest/webhook",
            json={"sender": "123", "message": "hola"}
        )

    async def test_enviar_a_rasa_sin_recipient_id_ni_text(self):
        mock_http_client = AsyncMock()
        mock_presentador = MagicMock()
        
        mock_presentador.a_payload_rasa.return_value = {"sender": "123", "message": "hola"}
        
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {}
        ]
        mock_http_client.post.return_value = mock_response
        
        gateway = GatewayRasa(
            http_client=mock_http_client,
            presentador=mock_presentador,
            rasa_url="http://localhost:5005"
        )
        
        mensaje_original = Message(
            conversation_id="123",
            content="hola",
            sender_id="user1",
            sender_role=SenderRole.USER,
            message_type=MessageType.INCOMING
        )
        
        resultado = await gateway.enviar_a_rasa(mensaje_original)
        
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].conversation_id, "123")
        self.assertEqual(resultado[0].content, "")

if __name__ == "__main__":
    unittest.main()
