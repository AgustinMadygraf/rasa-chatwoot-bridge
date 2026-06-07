"""
Path: src/application/pipeline.py
"""

from src.dominio.mensaje import Mensaje, TipoMensaje
from src.application.ports.logger import Logger

class MessagePipeline:
    def __init__(self, logger: Logger):
        self.logger = logger
        self.filters = [self.filter_outgoing_messages]

    def filter_outgoing_messages(self, message: Mensaje) -> bool:
        if message.tipo_mensaje == TipoMensaje.SALIENTE:
            self.logger.info(f"Filtro Pipeline: Mensaje OUTGOING (id={message.id_conversacion}) ignorado.")
            return False
        return True

    def should_process(self, message: Mensaje) -> bool:
        return all(f(message) for f in self.filters)
