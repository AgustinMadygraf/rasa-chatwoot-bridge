"""
Implementación del gateway de Chatwoot.
"""

from src.aplicacion.puertos.puerta_enlace_chatwoot import PuertaEnlaceChatwoot
from src.aplicacion.puertos.cliente_http import ClienteHTTP
from src.dominio.mensaje import Mensaje
from src.adaptadores.presentadores.presentador_chatwoot import PresentadorChatwootInterface

class GatewayChatwoot(PuertaEnlaceChatwoot):
    def __init__(self, cliente_http: ClienteHTTP, presentador: PresentadorChatwootInterface, base_url: str, api_token: str, account_id: str):
        self.cliente_http = cliente_http
        self.presentador = presentador
        self.base_url = base_url
        self.api_token = api_token
        self.account_id = account_id

    async def enviar_mensaje(self, mensaje: Mensaje) -> None:
        id_conversacion = mensaje.id_conversacion.valor
        url = f"{self.base_url}/api/v1/accounts/{self.account_id}/conversations/{id_conversacion}/messages"
        cabeceras = {"api_access_token": self.api_token}
        payload = self.presentador.a_payload_chatwoot(mensaje)
        await self.cliente_http.enviar(url, json=payload, cabeceras=cabeceras)
