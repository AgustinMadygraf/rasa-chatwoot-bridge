"""
Path: src/interface_adapters/mapeadores/mapeador_chatwoot.py
"""

from typing import Any, Dict
from src.dominio.mensaje import Mensaje, TipoMensaje, RolRemitente

class MapeadorChatwoot:
    @staticmethod
    def a_dominio(payload: Dict[str, Any]) -> Mensaje:
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
