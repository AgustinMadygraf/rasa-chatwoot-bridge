import unittest
from unittest.mock import MagicMock, AsyncMock
from src.application.orquestador import Orquestador
from src.dominio.mensaje import Mensaje, TipoMensaje, RolRemitente

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
        mensaje = Mensaje(
            id_conversacion="123",
            contenido="hola",
            id_remitente="user1",
            rol_remitente=RolRemitente.USUARIO,
            tipo_mensaje=TipoMensaje.ENTRANTE
        )
        
        respuesta_rasa = Mensaje(
            id_conversacion="123",
            contenido="hola soy rasa",
            id_remitente="bot",
            rol_remitente=RolRemitente.BOT,
            tipo_mensaje=TipoMensaje.SALIENTE
        )
        self.mock_rasa.enviar_a_rasa.return_value = [respuesta_rasa]

        await self.orquestador.manejar_mensaje_entrante(mensaje)

        self.mock_rasa.enviar_a_rasa.assert_called_once_with(mensaje)
        self.mock_chatwoot.enviar_mensaje.assert_called_once()
        self.mock_logger.info.assert_any_call("Orquestador procesando mensaje. Modo Rasa: True")

if __name__ == "__main__":
    unittest.main()
