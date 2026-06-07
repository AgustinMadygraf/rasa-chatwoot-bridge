import unittest
from unittest.mock import AsyncMock, MagicMock
from src.adaptadores.pasarelas.pasarela_rasa import PasarelaRasa
from src.dominio.mensaje import Mensaje, TipoMensaje, RolRemitente

class TestPasarelaRasa(unittest.IsolatedAsyncioTestCase):
    async def test_enviar_a_rasa_exito(self):
        mock_cliente_http = AsyncMock()
        mock_presentador = MagicMock()
        
        mock_presentador.a_payload_rasa.return_value = {"sender": "123", "message": "hola"}
        
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"recipient_id": "123", "text": "¡Hola! ¿En qué puedo ayudarte?"}
        ]
        mock_cliente_http.enviar.return_value = mock_response
        
        gateway = PasarelaRasa(
            cliente_http=mock_cliente_http,
            presentador=mock_presentador,
            rasa_url="http://localhost:5005"
        )
        
        mensaje_original = Mensaje(
            id_conversacion="123",
            contenido="hola",
            id_remitente="user1",
            rol_remitente=RolRemitente.USUARIO,
            tipo_mensaje=TipoMensaje.ENTRANTE
        )
        
        resultado = await gateway.enviar_a_rasa(mensaje_original)
        
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].id_conversacion.valor, "123")
        self.assertEqual(resultado[0].contenido, "¡Hola! ¿En qué puedo ayudarte?")
        self.assertEqual(resultado[0].id_remitente.valor, "bot")
        self.assertEqual(resultado[0].rol_remitente, RolRemitente.BOT)
        self.assertEqual(resultado[0].tipo_mensaje, TipoMensaje.SALIENTE)
        
        mock_cliente_http.enviar.assert_called_once_with(
            "http://localhost:5005/webhooks/rest/webhook",
            json={"sender": "123", "message": "hola"}
        )

    async def test_enviar_a_rasa_sin_recipient_id_ni_text(self):
        mock_cliente_http = AsyncMock()
        mock_presentador = MagicMock()
        
        mock_presentador.a_payload_rasa.return_value = {"sender": "123", "message": "hola"}
        
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"text": "respuesta válida"}
        ]
        mock_cliente_http.enviar.return_value = mock_response
        
        gateway = PasarelaRasa(
            cliente_http=mock_cliente_http,
            presentador=mock_presentador,
            rasa_url="http://localhost:5005"
        )
        
        mensaje_original = Mensaje(
            id_conversacion="123",
            contenido="hola",
            id_remitente="user1",
            rol_remitente=RolRemitente.USUARIO,
            tipo_mensaje=TipoMensaje.ENTRANTE
        )
        
        resultado = await gateway.enviar_a_rasa(mensaje_original)
        
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].id_conversacion.valor, "123")
        self.assertEqual(resultado[0].contenido, "respuesta válida")

if __name__ == "__main__":
    unittest.main()
