"""
Path: src/interface_adapters/gateways/gateway_chatwoot.py
"""

from src.application.ports.puerta_enlace_chatwoot import PuertaEnlaceChatwoot
from src.application.ports.http_client import HTTPClient
from src.domain.message import Message
from src.interface_adapters.presenters.presentador_chatwoot import PresentadorChatwoot

class GatewayChatwoot(PuertaEnlaceChatwoot):
    def __init__(self, http_client: HTTPClient, base_url: str, api_token: str, account_id: str):
        self.http_client = http_client
        self.base_url = base_url
        self.api_token = api_token
        self.account_id = account_id

    async def enviar_mensaje(self, conversation_id: str, message: Message) -> None:
        url = f"{self.base_url}/api/v1/accounts/{self.account_id}/conversations/{conversation_id}/messages"
        headers = {"api_access_token": self.api_token}
        payload = PresentadorChatwoot.a_payload_chatwoot(message)
        await self.http_client.post(url, json=payload, headers=headers)
