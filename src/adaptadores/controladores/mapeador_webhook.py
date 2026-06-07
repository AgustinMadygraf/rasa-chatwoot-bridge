# Path: src/adaptadores/controladores/mapeador_webhook.py

from typing import Any, Dict
from src.dominio.mensaje import Mensaje, TipoMensaje, RolRemitente

class MapeadorMensajeWebhook:
    @staticmethod
    def desde_payload_chatwoot(payload: Dict[str, Any]) -> Mensaje:
        raw_type = payload.get("message_type", "incoming")
        
        audio_url = None
        if raw_type == "audio":
            msg_type = TipoMensaje.AUDIO
            attachments = payload.get("attachments", [])
            if attachments:
                audio_url = attachments[0].get("data_url")
        else:
            msg_type = TipoMensaje.SALIENTE if raw_type == "outgoing" else TipoMensaje.ENTRANTE
            
        sender_id = str(payload["sender"]["id"])
        role = RolRemitente.BOT if msg_type == TipoMensaje.SALIENTE else RolRemitente.USUARIO
        
        return Mensaje.crear(
            id_conversacion=str(payload["conversation"]["id"]),
            contenido=payload.get("content") or "",
            id_remitente=sender_id,
            rol_remitente=role,
            tipo_mensaje=msg_type,
            audio_url=audio_url
        )
