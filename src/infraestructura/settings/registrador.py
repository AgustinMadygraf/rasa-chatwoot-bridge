# Path: src/infraestructura/settings/registrador.py

import logging
import sys
from src.aplicacion.puertos.registrador import Registrador
from src.infraestructura.settings.config import ajustes

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
    logger.setLevel(ajustes.nivel_log)
    
    handler = logging.StreamHandler(sys.stdout)
    # Formato más limpio: [HORA] [NIVEL] Mensaje
    formato = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='%H:%M:%S')
    handler.setFormatter(formato)
    
    if not logger.handlers:
        logger.addHandler(handler)
        
    return RegistradorAdapter(logger)

def configurar_logging_ngrok(logger: Registrador):
    # Silenciar logs ruidosos de dependencias
    for log_name in ['pyngrok', 'httpx', 'httpcore', 'uvicorn', 'uvicorn.access', 'uvicorn.error']:
        logging.getLogger(log_name).setLevel(logging.WARNING)

logger = configurar_logger()
