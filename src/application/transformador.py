"""
Path: src/application/transformador.py
"""

from typing import Any, Dict
from src.dominio.mensaje import Mensaje, TipoMensaje, RolRemitente

class TransformadorChatwoot:
    @staticmethod
    def a_dominio(payload: Dict[str, Any]) -> Mensaje:
        # Mapeo directo del tipo de mensaje de Chatwoot
        raw_type = payload.get("message_type", "incoming")
        msg_type = TipoMensaje.OUTGOING if raw_type == "outgoing" else TipoMensaje.INCOMING
        
        # Mapeo del rol (usamos outgoing para identificar el bot)
        sender_id = str(payload["sender"]["id"])
        
        # Si es outgoing, forzamos rol BOT para asegurar consistencia
        role = RolRemitente.BOT if msg_type == TipoMensaje.OUTGOING else RolRemitente.USER
        
        return Mensaje(
            id_conversacion=str(payload["conversation"]["id"]),
            contenido=payload.get("content") or "",
            id_remitente=sender_id,
            rol_remitente=role,
            tipo_mensaje=msg_type
        )
