import unittest
from unittest.mock import MagicMock, AsyncMock
from src.aplicacion.casos_de_uso.procesar_mensaje_entrante import ProcesarMensajeEntrante
from src.dominio.mensaje import Mensaje, TipoMensaje, RolRemitente

class TestProcesarMensajeEntrante(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.mock_chatwoot = AsyncMock()
        self.mock_rasa = AsyncMock()
        self.mock_asr = AsyncMock()
        self.mock_logger = MagicMock()
        self.caso_de_uso = ProcesarMensajeEntrante(
            puerta_enlace_chatwoot=self.mock_chatwoot, 
            puerta_enlace_rasa=self.mock_rasa,
            puerta_enlace_asr=self.mock_asr,
            usar_rasa=True, 
            logger=self.mock_logger
        )

    async def test_ejecutar_con_rasa(self):
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

        await self.caso_de_uso.ejecutar(mensaje)

        self.mock_rasa.enviar_a_rasa.assert_called_once_with(mensaje)
        # Verificamos que se llame con el objeto mensaje de respuesta, sin el ID redundante
        self.mock_chatwoot.enviar_mensaje.assert_called_once_with(respuesta_rasa)
        self.mock_logger.informar.assert_any_call("Procesando mensaje. Modo Rasa: True")

    async def test_ejecutar_audio_y_rasa(self):
        self.mock_asr.transcribir_audio.return_value = "hola transcrito"
        
        mensaje = Mensaje(
            id_conversacion="123",
            contenido="",
            id_remitente="user1",
            rol_remitente=RolRemitente.USUARIO,
            tipo_mensaje=TipoMensaje.AUDIO,
            audio_url="http://audio.url"
        )
        
        respuesta_rasa = Mensaje(
            id_conversacion="123",
            contenido="hola soy rasa",
            id_remitente="bot",
            rol_remitente=RolRemitente.BOT,
            tipo_mensaje=TipoMensaje.SALIENTE
        )
        self.mock_rasa.enviar_a_rasa.return_value = [respuesta_rasa]

        await self.caso_de_uso.ejecutar(mensaje)

        self.mock_asr.transcribir_audio.assert_called_once_with("http://audio.url")
        assert mensaje.contenido == "hola transcrito"
        assert mensaje.tipo_mensaje == TipoMensaje.ENTRANTE
        self.mock_rasa.enviar_a_rasa.assert_called_once()
        self.mock_chatwoot.enviar_mensaje.assert_called_once_with(respuesta_rasa)

    async def test_ejecutar_sin_rasa(self):
        self.caso_de_uso.usar_rasa = False
        mensaje = Mensaje(
            id_conversacion="123",
            contenido="hola",
            id_remitente="user1",
            rol_remitente=RolRemitente.USUARIO,
            tipo_mensaje=TipoMensaje.ENTRANTE
        )

        await self.caso_de_uso.ejecutar(mensaje)

        self.mock_rasa.enviar_a_rasa.assert_not_called()
        self.mock_chatwoot.enviar_mensaje.assert_called_once()
        sent_msg = self.mock_chatwoot.enviar_mensaje.call_args[0][0]
        assert sent_msg.contenido == "hola"
        assert sent_msg.id_conversacion.valor == "123"

if __name__ == "__main__":
    unittest.main()
