"""
Path: src/application/orquestador.py
"""

from typing import List
from src.domain.message import Message, MessageType, SenderRole
from src.application.ports.puerta_enlace_chatwoot import PuertaEnlaceChatwoot
from src.application.ports.puerta_enlace_rasa import PuertaEnlaceRasa
from src.application.pipeline import MessagePipeline
from src.infrastructure.settings.logger import logger

class Orquestador:
    def __init__(self, puerta_enlace_chatwoot: PuertaEnlaceChatwoot, puerta_enlace_rasa: PuertaEnlaceRasa, use_rasa: bool):
        self.puerta_enlace_chatwoot = puerta_enlace_chatwoot
        self.puerta_enlace_rasa = puerta_enlace_rasa
        self.use_rasa = use_rasa
        self.pipeline = MessagePipeline()

    async def manejar_mensaje_entrante(self, mensaje: Message) -> None:
        if not self.pipeline.should_process(mensaje):
            return

        logger.info(f"Orquestador procesando mensaje. Modo Rasa: {self.use_rasa}")
        if self.use_rasa:
            respuestas_rasa: List[Message] = await self.puerta_enlace_rasa.enviar_a_rasa(mensaje)
            for respuesta in respuestas_rasa:
                if respuesta.content:
                    await self._enviar_a_chatwoot(mensaje.conversation_id, respuesta.content)
        else:
            await self._enviar_a_chatwoot(mensaje.conversation_id, mensaje.content)

    async def _enviar_a_chatwoot(self, conv_id: str, content: str) -> None:
        mensaje_respuesta = Message(
            conversation_id=conv_id,
            content=content,
            sender_id="bot",
            sender_role=SenderRole.BOT,
            message_type=MessageType.OUTGOING
        )
        await self.puerta_enlace_chatwoot.enviar_mensaje(conv_id, mensaje_respuesta)
        logger.info("Mensaje enviado a Chatwoot.")
