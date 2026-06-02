"""
Path: src/infrastructure/httpx/puerta_enlace_chatwoot.py
"""

from httpx import AsyncClient

from src.domain.message import Message
from src.application.ports.puerta_enlace_chatwoot import PuertaEnlaceChatwoot

class HttpPuertaEnlaceChatwoot(PuertaEnlaceChatwoot):
    def __init__(self, base_url: str, api_token: str, account_id: str):
        self.base_url = base_url
        self.api_token = api_token
        self.account_id = account_id

    async def enviar_mensaje(self, conversation_id: str, message: Message) -> None:
        url = f"{self.base_url}/api/v1/accounts/{self.account_id}/conversations/{conversation_id}/messages"
        headers = {"api_access_token": self.api_token}
        payload = {"content": message.content, "message_type": "outgoing"}
        async with AsyncClient() as client:
            await client.post(url, json=payload, headers=headers)
