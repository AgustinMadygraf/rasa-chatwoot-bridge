"""
Path: src/interface_adapters/gateways/gateway_rasa.py
"""

from src.application.ports.puerta_enlace_rasa import PuertaEnlaceRasa
from src.application.ports.http_client import HTTPClient
from src.domain.message import Message
from src.interface_adapters.presenters.presentador_rasa import PresentadorRasa
from typing import List

class GatewayRasa(PuertaEnlaceRasa):
    def __init__(self, http_client: HTTPClient, rasa_url: str):
        self.http_client = http_client
        self.rasa_url = rasa_url

    async def enviar_a_rasa(self, message: Message) -> List[Message]:
        url = f"{self.rasa_url}/webhooks/rest/webhook"
        payload = PresentadorRasa.a_payload_rasa(message)
        response = await self.http_client.post(url, json=payload)
        return [Message(**msg) for msg in response.json()]
