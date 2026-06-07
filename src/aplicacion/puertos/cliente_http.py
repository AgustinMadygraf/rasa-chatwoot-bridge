# Path: src/aplicacion/puertos/cliente_http.py

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class RespuestaHTTP(ABC):
    @abstractmethod
    def json(self) -> Any: ...
    @property
    @abstractmethod
    def codigo_estado(self) -> int: ...
    @property
    @abstractmethod
    def contenido_binario(self) -> bytes: ...

class ClienteHTTP(ABC):
    @abstractmethod
    async def enviar(self, url: str, json: Optional[Dict[str, Any]] = None, cabeceras: Optional[Dict[str, str]] = None) -> RespuestaHTTP: ...
    @abstractmethod
    async def obtener(self, url: str, cabeceras: Optional[Dict[str, str]] = None) -> RespuestaHTTP: ...
