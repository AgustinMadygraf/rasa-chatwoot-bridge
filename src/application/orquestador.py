"""
Path: src/application/orquestador.py
"""

from typing import List
from src.domain.message import Message, MessageType
from src.application.ports.puerta_enlace_chatwoot import PuertaEnlaceChatwoot
from src.application.ports.puerta_enlace_rasa import PuertaEnlaceRasa
from src.infrastructure.settings.logger import logger

class Orquestador:
    def __init__(self, puerta_enlace_chatwoot: PuertaEnlaceChatwoot, puerta_enlace_rasa: PuertaEnlaceRasa, use_rasa: bool):
        self.puerta_enlace_chatwoot = puerta_enlace_chatwoot
        self.puerta_enlace_rasa = puerta_enlace_rasa
        self.use_rasa = use_rasa

    async def manejar_mensaje_entrante(self, mensaje: Message) -> None:
        logger.info(f"Orquestador recibiendo mensaje. Modo Rasa: {self.use_rasa}")
        if self.use_rasa:
            logger.info("Modo Rasa activo. Enviando a Rasa...")
            respuestas_rasa: List[Message] = await self.puerta_enlace_rasa.enviar_a_rasa(mensaje)
            for respuesta in respuestas_rasa:
                if respuesta.content:
                    mensaje_respuesta = Message(
                        conversation_id=mensaje.conversation_id,
                        content=respuesta.content,
                        sender_id="bot",
                        message_type=MessageType.OUTGOING
                    )
                    await self.puerta_enlace_chatwoot.enviar_mensaje(mensaje.conversation_id, mensaje_respuesta)
        else:
            logger.info("Modo espejo activo. Reflejando mensaje...")
            # Modo espejo: la respuesta es el mismo contenido del mensaje recibido
            mensaje_respuesta = Message(
                conversation_id=mensaje.conversation_id,
                content=mensaje.content,
                sender_id="bot",
                message_type=MessageType.OUTGOING
            )
            await self.puerta_enlace_chatwoot.enviar_mensaje(mensaje.conversation_id, mensaje_respuesta)
            logger.info("Mensaje reflejado enviado a Chatwoot.")
