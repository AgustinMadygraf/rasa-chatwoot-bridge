from typing import Any, Optional
from src.aplicacion.excepciones import AccesoNoAutorizadoError, ErrorProcesamientoWebhook
from src.infrastructure.settings.registrador import logger
from fastapi import APIRouter, Header, Request, Depends, HTTPException
from src.infrastructure.fastapi.dependencias import obtener_controlador_webhook

router = APIRouter()

@router.post('/webhook/chatwoot')
async def chatwoot_webhook(request: Request, x_webhook_token: Optional[str] = Header(None), controlador: Any = Depends(obtener_controlador_webhook)):
    payload = await request.json()
    logger.informar(f'PAYLOAD RECIBIDO: {payload}')
    try:
        return await controlador.manejar_webhook_chatwoot(payload, x_webhook_token)
    except AccesoNoAutorizadoError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except ErrorProcesamientoWebhook as e:
        logger.registrar_error(f'Error crítico procesando webhook: {str(e)}', exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
