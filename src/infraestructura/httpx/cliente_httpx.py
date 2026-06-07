# Path: src/infraestructura/httpx/cliente_httpx.py

from httpx import AsyncClient, Response
from typing import Any, Dict, Optional
from src.aplicacion.puertos.cliente_http import ClienteHTTP, RespuestaHTTP

class AdaptadorRespuestaHttpx(RespuestaHTTP):
    def __init__(self, response: Response):
        self._response = response

    def json(self) -> Any:
        return self._response.json()

    @property
    def codigo_estado(self) -> int:
        return self._response.status_code
        
    @property
    def contenido_binario(self) -> bytes:
        return self._response.content

class ClienteHttpx(ClienteHTTP):
    async def enviar(self, url: str, json: Optional[Dict[str, Any]] = None, cabeceras: Optional[Dict[str, str]] = None) -> RespuestaHTTP:
        async with AsyncClient() as client:
            response = await client.post(url, json=json, headers=cabeceras)
            return AdaptadorRespuestaHttpx(response)
            
    async def obtener(self, url: str, cabeceras: Optional[Dict[str, str]] = None) -> RespuestaHTTP:
        # Permitimos seguir redirecciones (302) configurando follow_redirects=True
        async with AsyncClient(follow_redirects=True) as client:
            response = await client.get(url, headers=cabeceras)
            return AdaptadorRespuestaHttpx(response)
