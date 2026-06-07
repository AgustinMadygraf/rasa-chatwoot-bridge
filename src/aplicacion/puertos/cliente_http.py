"""
Puerto para el cliente HTTP.
"""

from typing import Protocol, Any, Dict, Optional

class RespuestaHTTP(Protocol):
    def json(self) -> Any: ...
    @property
    def status_code(self) -> int: ...

class ClienteHTTP(Protocol):
    async def enviar(self, url: str, json: Optional[Dict[str, Any]] = None, cabeceras: Optional[Dict[str, str]] = None) -> RespuestaHTTP: ...
