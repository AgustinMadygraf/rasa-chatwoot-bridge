# Path: src/dominio/mensaje.py

from enum import Enum
from typing import Optional
from src.dominio.objetos_valor import IdConversacion, IdRemitente

class TipoMensaje(Enum):
    ENTRANTE = "incoming"
    SALIENTE = "outgoing"
    AUDIO = "audio"

class RolRemitente(Enum):
    USUARIO = "user"
    BOT = "bot"
    SISTEMA = "system"

class Mensaje:
    def __init__(
        self,
        id_conversacion: str,
        contenido: str,
        id_remitente: str,
        rol_remitente: RolRemitente,
        tipo_mensaje: TipoMensaje,
        audio_url: Optional[str] = None
    ):
        if not (contenido and contenido.strip()) and tipo_mensaje != TipoMensaje.AUDIO:
            raise ValueError("El contenido del mensaje no puede estar vacío.")
        
        self.id_conversacion = IdConversacion(id_conversacion)
        self.contenido = contenido
        self.id_remitente = IdRemitente(id_remitente)
        self.rol_remitente = rol_remitente
        self.tipo_mensaje = tipo_mensaje
        self.audio_url = audio_url

    @classmethod
    def crear(
        cls,
        id_conversacion: str,
        contenido: str,
        id_remitente: str,
        rol_remitente: RolRemitente,
        tipo_mensaje: TipoMensaje,
        audio_url: Optional[str] = None
    ) -> 'Mensaje':
        return cls(
            id_conversacion=id_conversacion,
            contenido=contenido,
            id_remitente=id_remitente,
            rol_remitente=rol_remitente,
            tipo_mensaje=tipo_mensaje,
            audio_url=audio_url
        )

    @classmethod
    def responder_como_bot(cls, id_conversacion: str, contenido: str) -> 'Mensaje':
        return cls(
            id_conversacion=id_conversacion,
            contenido=contenido,
            id_remitente='bot',
            rol_remitente=RolRemitente.BOT,
            tipo_mensaje=TipoMensaje.SALIENTE
        )

    def es_de_bot(self) -> bool:
        return self.rol_remitente == RolRemitente.BOT

    def es_procesable(self) -> bool:
        return self.tipo_mensaje == TipoMensaje.ENTRANTE or self.tipo_mensaje == TipoMensaje.AUDIO
