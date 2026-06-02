"""
Path: src/infrastructure/fastapi/rutas_webhook.py
"""

from typing import Any, Dict
from fastapi import APIRouter, Depends
from src.interface_adapters.controllers.controlador_webhook import ControladorWebhook

router = APIRouter()

def obtener_controlador() -> ControladorWebhook:
    raise NotImplementedError("Dependencia no inyectada")

@router.post("/webhook/chatwoot")
async def chatwoot_webhook(payload: Dict[str, Any], controlador: ControladorWebhook = Depends(obtener_controlador)):
    return await controlador.manejar_webhook_chatwoot(payload)
