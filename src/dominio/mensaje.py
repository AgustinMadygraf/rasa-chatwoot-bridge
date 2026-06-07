from enum import Enum
from src.dominio.objetos_valor import IdConversacion, IdRemitente

class TipoMensaje(Enum):
    ENTRANTE = "incoming"
    SALIENTE = "outgoing"

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
        tipo_mensaje: TipoMensaje
    ):
        if not contenido or not contenido.strip():
            raise ValueError("El contenido del mensaje no puede estar vacío.")
        
        # Envolviendo en Value Objects
        self.id_conversacion = IdConversacion(id_conversacion)
        self.contenido = contenido
        self.id_remitente = IdRemitente(id_remitente)
        self.rol_remitente = rol_remitente
        self.tipo_mensaje = tipo_mensaje

    def es_de_bot(self) -> bool:
        return self.rol_remitente == RolRemitente.BOT

    def es_procesable(self) -> bool:
        return self.tipo_mensaje == TipoMensaje.ENTRANTE
