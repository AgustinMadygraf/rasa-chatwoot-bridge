# Path: src/infraestructura/httpx/cliente_httpx.py

from httpx import AsyncClient
from typing import Any, Dict, Optional
from src.aplicacion.puertos.cliente_http import RespuestaHTTP

class AdaptadorRespuestaHttpx:
    def __init__(self, response):
        self._response = response

    def json(self) -> Any:
        return self._response.json()

    @property
    def codigo_estado(self) -> int:
        return self._response.status_code

class ClienteHttpx:
    async def enviar(self, url: str, json: Optional[Dict[str, Any]] = None, cabeceras: Optional[Dict[str, str]] = None) -> RespuestaHTTP:
        async with AsyncClient() as client:
            response = await client.post(url, json=json, headers=cabeceras)
            return AdaptadorRespuestaHttpx(response)
