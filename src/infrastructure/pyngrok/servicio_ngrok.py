"""
Path: src/infrastructure/pyngrok/servicio_ngrok.py
"""

from typing import Any, Dict
from pyngrok import ngrok
from src.infrastructure.settings.config import ajustes
from src.infrastructure.settings.logger import AppLogger

def iniciar_tunel(logger: AppLogger):
    """
    Inicializa el túnel de ngrok si está habilitado en la configuración.
    """
    if not ajustes.usar_ngrok:
        return None

    try:
        if ajustes.ngrok_auth_token:
            ngrok.set_auth_token(ajustes.ngrok_auth_token)
        
        opciones: Dict[str, Any] = {}
        if ajustes.ngrok_domain:
            opciones["domain"] = ajustes.ngrok_domain
            
        public_url = ngrok.connect(str(ajustes.app_port), **opciones).public_url
        # Este log es importante, por eso lo mantenemos en nuestro logger principal
        logger.info(f"Túnel ngrok abierto en: {public_url}")
        return public_url
    except Exception as e:
        logger.error(f"Error al iniciar el túnel de ngrok: {e}")
        return None
