from dataclasses import dataclass
from enum import Enum

class TipoMensaje(Enum):
    ENTRANTE = "incoming"
    SALIENTE = "outgoing"

class RolRemitente(Enum):
    USUARIO = "user"
    BOT = "bot"
    SISTEMA = "system"

class Mensaje:
    """Entidad de dominio que representa un mensaje en el sistema."""
    
    def __init__(
        self,
        id_conversacion: str,
        contenido: str,
        id_remitente: str,
        rol_remitente: RolRemitente,
        tipo_mensaje: TipoMensaje
    ):
        if not contenido or not contenido.strip():
            raise ValueError("El contenido del mensaje no puede estar vacío.")
        
        self.id_conversacion = id_conversacion
        self.contenido = contenido
        self.id_remitente = id_remitente
        self.rol_remitente = rol_remitente
        self.tipo_mensaje = tipo_mensaje

    def es_de_bot(self) -> bool:
        return self.rol_remitente == RolRemitente.BOT
