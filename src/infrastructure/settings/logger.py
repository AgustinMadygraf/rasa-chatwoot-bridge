"""
Path: src/infrastructure/settings/logger.py
"""

import logging
import sys

def configurar_logger():
    logger = logging.getLogger("puente_rasa_chatwoot")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    formato = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formato)
    logger.addHandler(handler)
    return logger

logger = configurar_logger()
