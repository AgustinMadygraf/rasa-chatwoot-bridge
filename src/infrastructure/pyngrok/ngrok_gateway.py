from typing import Any, Dict, Optional
from pyngrok import ngrok
from src.infrastructure.settings.registrador import configurar_logging_ngrok
from src.infrastructure.settings.config import ajustes
from src.aplicacion.puertos.registrador import Registrador
from src.aplicacion.puertos.servicio_tunel import ServicioTunel

class NgrokGateway(ServicioTunel):
    def iniciar(self, logger: Registrador) -> Optional[str]:
        if not ajustes.usar_ngrok:
            return None
        configurar_logging_ngrok(logger)
        
        try:
            if ajustes.ngrok_auth_token:
                ngrok.set_auth_token(ajustes.ngrok_auth_token)
            
            tunnels = ngrok.get_tunnels()
            for tunnel in tunnels:
                # Corrección: Verificar que public_url no sea None antes de usar endswith
                if tunnel.public_url:
                    if ajustes.ngrok_domain and tunnel.public_url.endswith(ajustes.ngrok_domain):
                        logger.informar(f'Reutilizando túnel existente: {tunnel.public_url}')
                        return tunnel.public_url
                    if not ajustes.ngrok_domain and tunnel.config.get('addr') == f'localhost:{ajustes.app_port}':
                        logger.informar(f'Reutilizando túnel existente: {tunnel.public_url}')
                        return tunnel.public_url

            opciones: Dict[str, Any] = {}
            if ajustes.ngrok_domain:
                opciones['domain'] = ajustes.ngrok_domain
            
            resultado = ngrok.connect(str(ajustes.app_port), **opciones)
            public_url = resultado.public_url
            if public_url:
                logger.informar(f'Túnel ngrok abierto en: {public_url}')
            return public_url
            
        except Exception as e:
            logger.registrar_error(f'Error al iniciar el túnel de ngrok: {e}')
            return None

    def cerrar(self):
        ngrok.kill()
