"""
Path: src/interface_adapters/presenters/presentador_webhook.py
"""

from typing import Dict

class PresentadorWebhook:
    @staticmethod
    def respuesta_exitosa() -> Dict[str, str]:
        return {"status": "ok", "message": "Procesado correctamente"}

    @staticmethod
    def respuesta_error(mensaje: str) -> Dict[str, str]:
        return {"status": "error", "message": mensaje}
