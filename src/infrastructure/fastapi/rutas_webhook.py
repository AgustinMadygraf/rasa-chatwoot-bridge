"""
Path: src/infrastructure/fastapi/rutas_webhook.py
"""

from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, Query
from src.interface_adapters.controllers.controlador_webhook import ControladorWebhook

router = APIRouter()

# Variable global para almacenar el controlador inyectado
_controlador: Optional[ControladorWebhook] = None

def set_controlador(controlador: ControladorWebhook):
    global _controlador
    _controlador = controlador

def obtener_controlador() -> ControladorWebhook:
    if _controlador is None:
        raise NotImplementedError("Controlador no inyectado")
    return _controlador

@router.post("/webhook/chatwoot")
async def chatwoot_webhook(
    payload: Dict[str, Any], 
    token: Optional[str] = Query(None),
    controlador: ControladorWebhook = Depends(obtener_controlador)
):
    return await controlador.manejar_webhook_chatwoot(payload, token=token)
