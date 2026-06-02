"""
Path: src/infrastructure/fastapi/rutas_webhook.py
"""

from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, Query
from src.interface_adapters.controllers.controlador_webhook import ControladorWebhook
from src.infrastructure.fastapi.dependencias import obtener_controlador_webhook

router = APIRouter()

@router.post("/webhook/chatwoot")
async def chatwoot_webhook(
    payload: Dict[str, Any], 
    token: Optional[str] = Query(None),
    controlador: ControladorWebhook = Depends(obtener_controlador_webhook)
):
    return await controlador.manejar_webhook_chatwoot(payload, token=token)
