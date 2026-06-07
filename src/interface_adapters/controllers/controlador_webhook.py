from typing import Any, Dict, Optional
from src.aplicacion.casos_de_uso.procesar_mensaje_entrante import ProcesarMensajeEntrante
from src.interface_adapters.mapeadores.mapeador_chatwoot import MapeadorChatwoot
from src.aplicacion.exceptions import AccesoNoAutorizadoError, ErrorProcesamientoWebhook
from src.dominio.mensaje import Mensaje
from src.interface_adapters.presenters.presentador_webhook import PresentadorWebhookInterface

class ControladorWebhook:
    def __init__(self, caso_de_uso: ProcesarMensajeEntrante, presentador: PresentadorWebhookInterface, webhook_token: Optional[str] = None):
        self.caso_de_uso = caso_de_uso
        self.presentador = presentador
        self.webhook_token = webhook_token

    async def manejar_webhook_chatwoot(self, payload: Dict[str, Any], token: Optional[str] = None) -> Dict[str, Any]:
        if self.webhook_token and token != self.webhook_token:
            raise AccesoNoAutorizadoError("Token de validación inválido")

        try:
            mensaje: Mensaje = MapeadorChatwoot.a_dominio(payload)
            await self.caso_de_uso.ejecutar(mensaje)
            return self.presentador.respuesta_exitosa()
        except ErrorProcesamientoWebhook:
            raise
        except Exception as e:
            raise ErrorProcesamientoWebhook(f"Error procesando webhook: {str(e)}")
