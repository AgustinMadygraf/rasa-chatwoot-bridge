# Path: src/interface_adapters/controllers/controlador_webhook.py

from typing import Any, Dict, Optional
from src.aplicacion.casos_de_uso.procesar_mensaje_entrante import ProcesarMensajeEntrante
from src.aplicacion.excepciones import AccesoNoAutorizadoError, ErrorProcesamientoWebhook
from src.dominio.mensaje import Mensaje, TipoMensaje, RolRemitente
from src.adaptadores.presentadores.presentador_webhook import PresentadorWebhookInterface

class ControladorWebhook:
    def __init__(self, caso_de_uso: ProcesarMensajeEntrante, presentador: PresentadorWebhookInterface, webhook_token: Optional[str] = None):
        self.caso_de_uso = caso_de_uso
        self.presentador = presentador
        self.webhook_token = webhook_token

    @staticmethod
    def _mapear_a_dominio(payload: Dict[str, Any]) -> Mensaje:
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

    async def manejar_webhook_chatwoot(self, payload: Dict[str, Any], token: Optional[str] = None) -> Dict[str, Any]:
        if self.webhook_token and token != self.webhook_token:
            raise AccesoNoAutorizadoError("Token de validación inválido")

        try:
            mensaje = self._mapear_a_dominio(payload)
            await self.caso_de_uso.ejecutar(mensaje)
            return self.presentador.respuesta_exitosa()
        except ErrorProcesamientoWebhook:
            raise
        except Exception as e:
            raise ErrorProcesamientoWebhook(f"Error procesando webhook: {str(e)}")
