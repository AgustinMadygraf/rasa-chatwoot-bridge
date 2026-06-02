"""
Path: src/infrastructure/httpx/puerta_enlace_rasa.py
"""

import httpx
from typing import List

from src.domain.message import Message
from src.application.ports.puerta_enlace_rasa import PuertaEnlaceRasa

class HttpPuertaEnlaceRasa(PuertaEnlaceRasa):
    def __init__(self, rasa_url: str):
        self.rasa_url = rasa_url

    async def enviar_a_rasa(self, message: Message) -> List[Message]:
        url = f"{self.rasa_url}/webhooks/rest/webhook"
        payload = {"sender": message.conversation_id, "message": message.content}
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            return [Message(**msg) for msg in response.json()]
