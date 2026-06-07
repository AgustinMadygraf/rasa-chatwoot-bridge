"""
Path: src/aplicacion/casos_de_uso/procesar_mensaje_entrante.py
"""

from typing import List
from src.dominio.mensaje import Mensaje
from src.aplicacion.puertos.puerta_enlace_chatwoot import PuertaEnlaceChatwoot
from src.aplicacion.puertos.puerta_enlace_rasa import PuertaEnlaceRasa
from src.aplicacion.puertos.registrador import Registrador
from src.aplicacion.excepciones import ErrorProcesamientoWebhook

class ProcesarMensajeEntrante:
    def __init__(self, puerta_enlace_chatwoot: PuertaEnlaceChatwoot, puerta_enlace_rasa: PuertaEnlaceRasa, usar_rasa: bool, logger: Registrador):
        self.puerta_enlace_chatwoot = puerta_enlace_chatwoot
        self.puerta_enlace_rasa = puerta_enlace_rasa
        self.usar_rasa = usar_rasa
        self.logger = logger

    async def ejecutar(self, mensaje: Mensaje) -> None:
        if not mensaje.es_procesable():
            return

        self.logger.informar(f'Procesando mensaje. Modo Rasa: {self.usar_rasa}')
        try:
            if self.usar_rasa:
                respuestas_rasa: List[Mensaje] = await self.puerta_enlace_rasa.enviar_a_rasa(mensaje)
                for respuesta in respuestas_rasa:
                    if respuesta.contenido:
                        await self._enviar_a_chatwoot(mensaje.id_conversacion.valor, respuesta.contenido)
            else:
                await self._enviar_a_chatwoot(mensaje.id_conversacion.valor, mensaje.contenido)
        except Exception as e:
            self.logger.registrar_error(f'Error en caso de uso: {str(e)}')
            raise ErrorProcesamientoWebhook(f'Error procesando mensaje: {str(e)}')

    async def _enviar_a_chatwoot(self, id_conv: str, contenido: str) -> None:
        mensaje_respuesta = Mensaje.responder(id_conv, contenido)
        await self.puerta_enlace_chatwoot.enviar_mensaje(id_conv, mensaje_respuesta)
        self.logger.informar('Mensaje enviado a Chatwoot.')
