"""
Path: src/infrastructure/httpx/cliente_httpx.py
"""

from httpx import AsyncClient
from typing import Any, Dict, Optional
from src.application.ports.http_client import HTTPResponse

class HttpxClient:
    async def post(self, url: str, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> HTTPResponse:
        async with AsyncClient() as client:
            response = await client.post(url, json=json, headers=headers)
            return response
