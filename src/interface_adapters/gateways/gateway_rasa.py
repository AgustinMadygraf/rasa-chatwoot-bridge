"""
Path: src/interface_adapters/gateways/gateway_rasa.py
"""

from typing import List
from src.application.ports.puerta_enlace_rasa import PuertaEnlaceRasa
from src.application.ports.http_client import HTTPClient
from src.dominio.mensaje import Mensaje, TipoMensaje, RolRemitente
from src.interface_adapters.presenters.presentador_rasa import PresentadorRasaInterface

class GatewayRasa(PuertaEnlaceRasa):
    def __init__(self, http_client: HTTPClient, presentador: PresentadorRasaInterface, rasa_url: str):
        self.http_client = http_client
        self.presentador = presentador
        self.rasa_url = rasa_url

    async def enviar_a_rasa(self, message: Mensaje) -> List[Mensaje]:
        url = f"{self.rasa_url}/webhooks/rest/webhook"
        payload = self.presentador.a_payload_rasa(message)
        response = await self.http_client.post(url, json=payload)
        
        mensajes: List[Mensaje] = []
        for msg in response.json():
            recipient_id = msg.get("recipient_id") or message.id_conversacion.valor
            content = msg.get("text") or " "
            
            mensajes.append(
                Mensaje(
                    id_conversacion=str(recipient_id),
                    contenido=content,
                    id_remitente="bot",
                    rol_remitente=RolRemitente.BOT,
                    tipo_mensaje=TipoMensaje.SALIENTE
                )
            )
        return mensajes

