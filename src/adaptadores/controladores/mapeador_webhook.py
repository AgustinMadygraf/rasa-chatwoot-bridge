# Path: src/adaptadores/controladores/mapeador_webhook.py

from typing import Any, Dict
from src.dominio.mensaje import Mensaje, TipoMensaje, RolRemitente

class MapeadorMensajeWebhook:
    @staticmethod
    def desde_payload_chatwoot(payload: Dict[str, Any]) -> Mensaje:
        attachments = payload.get("attachments", [])
        
        # Detectar si es audio por adjuntos, incluso si el message_type no es "audio"
        audio_url = None
        if attachments:
            for attachment in attachments:
                if attachment.get("file_type") in ["audio", "video"]: # Chatwoot a veces etiqueta voz como video
                    audio_url = attachment.get("data_url")
                    break
        
        if audio_url:
            msg_type = TipoMensaje.AUDIO
        else:
            raw_type = payload.get("message_type", "incoming")
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
