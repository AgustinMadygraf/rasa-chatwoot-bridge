from typing import List
from src.dominio.mensaje import Mensaje, TipoMensaje, RolRemitente
from src.application.ports.puerta_enlace_chatwoot import PuertaEnlaceChatwoot
from src.application.ports.puerta_enlace_rasa import PuertaEnlaceRasa
from src.application.ports.logger import Logger
from src.application.exceptions import ErrorProcesamientoWebhook

class ProcesarMensajeEntrante:
    def __init__(self, puerta_enlace_chatwoot: PuertaEnlaceChatwoot, puerta_enlace_rasa: PuertaEnlaceRasa, use_rasa: bool, logger: Logger):
        self.puerta_enlace_chatwoot = puerta_enlace_chatwoot
        self.puerta_enlace_rasa = puerta_enlace_rasa
        self.use_rasa = use_rasa
        self.logger = logger

    async def ejecutar(self, mensaje: Mensaje) -> None:
        if not mensaje.es_procesable():
            return

        self.logger.info(f"Procesando mensaje. Modo Rasa: {self.use_rasa}")
        try:
            if self.use_rasa:
                respuestas_rasa: List[Mensaje] = await self.puerta_enlace_rasa.enviar_a_rasa(mensaje)
                for respuesta in respuestas_rasa:
                    if respuesta.contenido:
                        await self._enviar_a_chatwoot(mensaje.id_conversacion.valor, respuesta.contenido)
            else:
                await self._enviar_a_chatwoot(mensaje.id_conversacion.valor, mensaje.contenido)
        except Exception as e:
            self.logger.error(f"Error en caso de uso: {str(e)}")
            raise ErrorProcesamientoWebhook(f"Error procesando mensaje: {str(e)}")

    async def _enviar_a_chatwoot(self, conv_id: str, content: str) -> None:
        mensaje_respuesta = Mensaje(
            id_conversacion=conv_id,
            contenido=content,
            id_remitente="bot",
            rol_remitente=RolRemitente.BOT,
            tipo_mensaje=TipoMensaje.SALIENTE
        )
        await self.puerta_enlace_chatwoot.enviar_mensaje(conv_id, mensaje_respuesta)
        self.logger.info("Mensaje enviado a Chatwoot.")
