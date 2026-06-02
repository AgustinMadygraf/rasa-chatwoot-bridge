import logging
from typing import Any, Dict
from pyngrok import ngrok
from src.infrastructure.settings.config import ajustes
from src.infrastructure.settings.logger import logger

def configurar_logging_ngrok():
    """
    Configura el logger de la librería pyngrok para que sea visible.
    """
    logger_ngrok = logging.getLogger("pyngrok")
    logger_ngrok.setLevel(logging.INFO)
    
    if logger.handlers:
        for handler in logger.handlers:
            logger_ngrok.addHandler(handler)

def iniciar_tunel():
    """
    Inicializa el túnel de ngrok si está habilitado en la configuración.
    """
    if not ajustes.usar_ngrok:
        return None

    configurar_logging_ngrok()

    try:
        if ajustes.ngrok_auth_token:
            ngrok.set_auth_token(ajustes.ngrok_auth_token)

        opciones: Dict[str, Any] = {}
        if ajustes.ngrok_domain:
            opciones["domain"] = ajustes.ngrok_domain
            
        public_url = ngrok.connect(str(ajustes.app_port), **opciones).public_url
        logger.info(f"Túnel ngrok abierto en: {public_url}")
        return public_url
    except Exception as e:
        logger.error(f"Error al iniciar el túnel de ngrok: {e}")
        return None
