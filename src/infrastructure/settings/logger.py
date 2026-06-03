"""
Path: src/infrastructure/settings/logger.py
"""

import logging
import sys
from typing import Protocol, List

class AppLogger(Protocol):
    def info(self, msg: str) -> None: ...
    def error(self, msg: str) -> None: ...
    @property
    def handlers(self) -> List[logging.Handler]: ...

def configurar_logger() -> logging.Logger:
    logger = logging.getLogger("puente_rasa_chatwoot")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formato = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formato)
    logger.addHandler(handler)
    return logger

def configurar_logging_ngrok(logger: AppLogger):
    logger_ngrok = logging.getLogger("pyngrok")
    logger_ngrok.setLevel(logging.WARNING)

    logging.getLogger("pyngrok.process.ngrok").setLevel(logging.WARNING)

    if logger.handlers:
        for handler in logger.handlers:
            logger_ngrok.addHandler(handler)

logger = configurar_logger()
