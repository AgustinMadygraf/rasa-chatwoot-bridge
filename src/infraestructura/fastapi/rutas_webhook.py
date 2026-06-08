# Path: src/infraestructura/fastapi/rutas_webhook.py

from typing import Any, Optional
from src.aplicacion.excepciones import AccesoNoAutorizadoError, ErrorProcesamientoWebhook
from src.infraestructura.settings.registrador import logger
from fastapi import APIRouter, Header, Request, Depends, HTTPException
from src.infraestructura.fastapi.dependencias import obtener_controlador_webhook

router = APIRouter()

@router.post('/webhook/chatwoot')
async def chatwoot_webhook(request: Request, x_webhook_token: Optional[str] = Header(None), controlador: Any = Depends(obtener_controlador_webhook)):
    payload = await request.json()
    
    # Log completo del payload para depuración
    logger.depurar(f'PAYLOAD COMPLETO RECIBIDO: {payload}')
    
    # Log informativo resumido para reducir el ruido en la CLI
    evento = payload.get('event', 'desconocido')
    conversacion = payload.get('conversation', {})
    conv_id = conversacion.get('id', 'N/A')
    
    sender = payload.get('sender', {})
    remitente = sender.get('name', 'N/A')
    
    contenido = payload.get('content', '')
    contenido_resumido = (contenido[:60] + '...') if contenido and len(contenido) > 60 else (contenido or '')
    
    logger.informar(f"Webhook recibido -> Evento: '{evento}' | Conv: #{conv_id} | Remitente: {remitente} | Mensaje: '{contenido_resumido}'")
    
    try:
        return await controlador.manejar_webhook_chatwoot(payload, x_webhook_token)
    except AccesoNoAutorizadoError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except ErrorProcesamientoWebhook as e:
        logger.registrar_error(f'Error crítico procesando webhook: {str(e)}', exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
