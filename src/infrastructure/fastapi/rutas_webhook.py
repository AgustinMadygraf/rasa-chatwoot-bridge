"""
Path: src/infrastructure/fastapi/rutas_webhook.py
"""

from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, status
from src.interface_adapters.controllers.controlador_webhook import ControladorWebhook
from src.infrastructure.fastapi.dependencias import obtener_controlador_webhook
from src.infrastructure.settings.logger import logger
from src.application.exceptions import ErrorProcesamientoWebhook

router = APIRouter()

@router.post("/webhook/chatwoot")
async def chatwoot_webhook(
    payload: Dict[str, Any], 
    controlador: ControladorWebhook = Depends(obtener_controlador_webhook)
):
    # Log para depuración: Inspeccionar el payload recibido
    logger.info(f"PAYLOAD RECIBIDO: {payload}")
    
    try:
        return await controlador.manejar_webhook_chatwoot(payload)
    except ErrorProcesamientoWebhook as e:
        logger.error(f"Error crítico procesando webhook: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
