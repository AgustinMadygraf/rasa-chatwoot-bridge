# Path: src/adaptadores/pasarelas/pasarela_rasa.py

from typing import List
from src.aplicacion.puertos.puerta_enlace_rasa import PuertaEnlaceRasa
from src.aplicacion.puertos.cliente_http import ClienteHTTP
from src.dominio.mensaje import Mensaje, TipoMensaje, RolRemitente
from src.adaptadores.presentadores.presentador_rasa import PresentadorRasaInterface

class PasarelaRasa(PuertaEnlaceRasa):
    def __init__(self, cliente_http: ClienteHTTP, presentador: PresentadorRasaInterface, rasa_url: str):
        self.cliente_http = cliente_http
        self.presentador = presentador
        self.rasa_url = rasa_url

    async def enviar_a_rasa(self, mensaje: Mensaje) -> List[Mensaje]:
        url = f'{self.rasa_url}/webhooks/rest/webhook'
        payload = self.presentador.a_payload_rasa(mensaje)
        respuesta = await self.cliente_http.enviar(url, json=payload)
        
        mensajes: List[Mensaje] = []
        for msg in respuesta.json():
            recipient_id = msg.get('recipient_id') or mensaje.id_conversacion.valor
            raw_content = msg.get('text')
            
            if raw_content:
                try:
                    mensajes.append(Mensaje.crear(
                        id_conversacion=str(recipient_id),
                        contenido=raw_content,
                        id_remitente='bot',
                        rol_remitente=RolRemitente.BOT,
                        tipo_mensaje=TipoMensaje.SALIENTE
                    ))
                except ValueError:
                    continue
        return mensajes
