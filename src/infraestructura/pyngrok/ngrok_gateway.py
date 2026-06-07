# Path: infraestructura/pyngrok/ngrok_gateway.py

from typing import Any, Dict, Optional
from pyngrok import ngrok  # type: ignore
from src.infraestructura.settings.registrador import configurar_logging_ngrok
from src.infraestructura.settings.config import ajustes
from src.aplicacion.puertos.registrador import Registrador
from src.aplicacion.puertos.servicio_tunel import ServicioTunel

class PasarelaNgrok(ServicioTunel):
    def iniciar(self, logger: Registrador) -> Optional[str]:
        if not ajustes.usar_ngrok:
            return None
        configurar_logging_ngrok(logger)
        
        try:
            if ajustes.token_auth_ngrok:
                ngrok.set_auth_token(ajustes.token_auth_ngrok)
            
            tunnels = ngrok.get_tunnels()
            for tunnel in tunnels:
                # Corrección: Verificar que public_url no sea None antes de usar endswith
                if tunnel.public_url:
                    if ajustes.dominio_ngrok and tunnel.public_url.endswith(ajustes.dominio_ngrok):
                        logger.informar(f'Reutilizando túnel existente: {tunnel.public_url}')
                        return tunnel.public_url
                    if not ajustes.dominio_ngrok and tunnel.config.get('addr') == f'localhost:{ajustes.puerto_aplicacion}':
                        logger.informar(f'Reutilizando túnel existente: {tunnel.public_url}')
                        return tunnel.public_url

            opciones: Dict[str, Any] = {}
            if ajustes.dominio_ngrok:
                opciones['domain'] = ajustes.dominio_ngrok
            
            resultado = ngrok.connect(str(ajustes.puerto_aplicacion), **opciones)
            public_url = resultado.public_url
            if public_url:
                logger.informar(f'Túnel ngrok abierto en: {public_url}')
            return public_url
            
        except Exception as e:
            logger.registrar_error(f'Error al iniciar el túnel de ngrok: {e}')
            return None

    def cerrar(self):
        ngrok.kill()
