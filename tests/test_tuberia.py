import unittest
from unittest.mock import MagicMock
from src.application.tuberia import TuberiaMensajes
from src.dominio.mensaje import Mensaje, TipoMensaje, RolRemitente

class TestTuberiaMensajes(unittest.TestCase):
    def setUp(self):
        self.mock_logger = MagicMock()
        self.pipeline = TuberiaMensajes(self.mock_logger)

    def test_should_process_incoming_message(self):
        message = Mensaje(
            id_conversacion="123",
            contenido="hola",
            id_remitente="user1",
            rol_remitente=RolRemitente.USUARIO,
            tipo_mensaje=TipoMensaje.ENTRANTE
        )
        self.assertTrue(self.pipeline.should_process(message))

    def test_should_not_process_outgoing_message(self):
        message = Mensaje(
            id_conversacion="123",
            contenido="respuesta",
            id_remitente="bot",
            rol_remitente=RolRemitente.BOT,
            tipo_mensaje=TipoMensaje.SALIENTE
        )
        self.assertFalse(self.pipeline.should_process(message))
        self.mock_logger.info.assert_called_once()
        self.assertIn("ignorado", self.mock_logger.info.call_args[0][0])

if __name__ == "__main__":
    unittest.main()
