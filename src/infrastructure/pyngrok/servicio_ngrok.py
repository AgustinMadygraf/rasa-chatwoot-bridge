from pyngrok import ngrok
from src.infrastructure.settings.config import ajustes
from src.infrastructure.settings.logger import logger

def iniciar_tunel():
    """
    Inicializa el túnel de ngrok si está habilitado en la configuración.
    """
    if not ajustes.usar_ngrok:
        return None

    try:
        if ajustes.ngrok_auth_token:
            ngrok.set_auth_token(ajustes.ngrok_auth_token)
        
        # Se convierte el puerto a string para cumplir con el tipo esperado por pyngrok
        public_url = ngrok.connect(str(ajustes.app_port)).public_url
        logger.info(f"Túnel ngrok abierto en: {public_url}")
        print(f" * Túnel ngrok abierto en: {public_url}")
        return public_url
    except Exception as e:
        logger.error(f"Error al iniciar el túnel de ngrok: {e}")
        return None
