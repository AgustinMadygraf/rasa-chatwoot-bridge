# Path: src/infraestructura/registrador.py

import logging
import sys
from typing import Optional
from src.aplicacion.puertos.registrador import Registrador

class RegistradorAdapter:
    def __init__(self, logger: logging.Logger):
        self._logger = logger

    def informar(self, msg: str) -> None:
        self._logger.info(msg)

    def registrar_error(self, msg: str, exc_info: bool = False) -> None:
        self._logger.error(msg, exc_info=exc_info)

    def depurar(self, msg: str) -> None:
        self._logger.debug(msg)

    def advertir(self, msg: str) -> None:
        self._logger.warning(msg)

def configurar_logger() -> Registrador:
    logger = logging.getLogger('puente_rasa_chatwoot')
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formato = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formato)
    logger.addHandler(handler)
    return RegistradorAdapter(logger)

def configurar_logging_ngrok(logger: Registrador = None):
    logger_ngrok = logging.getLogger('pyngrok')
    logger_ngrok.setLevel(logging.WARNING)
    logging.getLogger('pyngrok.process.ngrok').setLevel(logging.WARNING)

logger = configurar_logger()
