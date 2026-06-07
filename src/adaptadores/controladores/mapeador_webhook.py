# Path: src/adaptadores/controladores/mapeador_webhook.py

from typing import Any, Dict
from src.dominio.mensaje import Mensaje, TipoMensaje, RolRemitente

class MapeadorMensajeWebhook:
    @staticmethod
    def desde_payload_chatwoot(payload: Dict[str, Any]) -> Mensaje:
        raw_type = payload.get("message_type", "incoming")
        msg_type = TipoMensaje.SALIENTE if raw_type == "outgoing" else TipoMensaje.ENTRANTE
        sender_id = str(payload["sender"]["id"])
        role = RolRemitente.BOT if msg_type == TipoMensaje.SALIENTE else RolRemitente.USUARIO
        
        return Mensaje.crear_asegurando_contenido(
            id_conversacion=str(payload["conversation"]["id"]),
            contenido=payload.get("content"),
            id_remitente=sender_id,
            rol_remitente=role,
            tipo_mensaje=msg_type
        )
