"""
Path: src/infrastructure/fastapi/rutas_webhook.py
"""

from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, Query, HTTPException, status
from src.interface_adapters.controllers.controlador_webhook import ControladorWebhook
from src.infrastructure.fastapi.dependencias import obtener_controlador_webhook
from src.infrastructure.settings.logger import logger
from src.application.exceptions import AccesoNoAutorizadoError, ErrorProcesamientoWebhook

router = APIRouter()

@router.post("/webhook/chatwoot")
async def chatwoot_webhook(
    payload: Dict[str, Any], 
    token: Optional[str] = Query(None),
    controlador: ControladorWebhook = Depends(obtener_controlador_webhook)
):
    try:
        return await controlador.manejar_webhook_chatwoot(payload, token=token)
    except AccesoNoAutorizadoError as e:
        logger.warning(f"Intento de acceso no autorizado: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except ErrorProcesamientoWebhook as e:
        logger.error(f"Error crítico procesando webhook: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
