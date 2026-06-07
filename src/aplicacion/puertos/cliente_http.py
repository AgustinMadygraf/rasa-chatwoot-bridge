# Path: src/aplicacion/puertos/cliente_http.py

from typing import Protocol, Any, Dict, Optional

class RespuestaHTTP(Protocol):
    def json(self) -> Any: ...
    @property
    def codigo_estado(self) -> int: ...

class ClienteHTTP(Protocol):
    async def enviar(self, url: str, json: Optional[Dict[str, Any]] = None, cabeceras: Optional[Dict[str, str]] = None) -> RespuestaHTTP: ...
