"""
Path: src/interface_adapters/presenters/presentador_webhook.py
"""

from typing import Dict, Protocol

class PresentadorWebhookInterface(Protocol):
    def respuesta_exitosa(self) -> Dict[str, str]:
        ...

    def respuesta_registrar_error(self, mensaje: str) -> Dict[str, str]:
        ...

class PresentadorWebhook:
    def respuesta_exitosa(self) -> Dict[str, str]:
        return {"status": "ok", "message": "Procesado correctamente"}

    def respuesta_registrar_error(self, mensaje: str) -> Dict[str, str]:
        return {"status": "error", "message": mensaje}
