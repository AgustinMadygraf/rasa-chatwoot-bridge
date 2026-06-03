"""
Path: src/application/ports/http_client.py
"""

from typing import Protocol, Any, Dict, Optional

class HTTPResponse(Protocol):
    def json(self) -> Any: ...
    @property
    def status_code(self) -> int: ...

class HTTPClient(Protocol):
    async def post(self, url: str, json: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> HTTPResponse: ...
