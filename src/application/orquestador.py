"""
Path: src/application/orquestador.py
"""

from typing import Any, Dict, List, cast
from src.interface_adapters.gateways.puerta_enlace_chatwoot import PuertaEnlaceChatwoot
from src.interface_adapters.gateways.puerta_enlace_rasa import PuertaEnlaceRasa
from src.domain.entities.message import Message, MessageType

class Orquestador:
    def __init__(self, puerta_enlace_chatwoot: PuertaEnlaceChatwoot, puerta_enlace_rasa: PuertaEnlaceRasa):
        self.puerta_enlace_chatwoot = puerta_enlace_chatwoot
        self.puerta_enlace_rasa = puerta_enlace_rasa

    async def manejar_mensaje_entrante(self, mensaje: Message) -> None:
        respuestas_rasa = cast(List[Dict[str, Any]], await self.puerta_enlace_rasa.enviar_a_rasa(mensaje))  # type: ignore[reportUnknownMemberType]
        for respuesta in respuestas_rasa:
            if "text" in respuesta:
                mensaje_respuesta = Message(
                    conversation_id=mensaje.conversation_id,
                    content=respuesta["text"],
                    sender_id="bot",
                    message_type=MessageType.OUTGOING
                )
                await self.puerta_enlace_chatwoot.enviar_mensaje(mensaje.conversation_id, mensaje_respuesta)
