from httpx import AsyncClient
from typing import Any, Dict, Optional
from src.aplicacion.puertos.cliente_http import RespuestaHTTP

class HttpxClient:
    async def enviar(self, url: str, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> RespuestaHTTP:
        async with AsyncClient() as client:
            response = await client.post(url, json=json, headers=headers)
            return response
