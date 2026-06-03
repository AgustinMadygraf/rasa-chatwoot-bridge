"""
Path: src/infrastructure/pyngrok/ngrok_gateway.py
"""

from typing import Any, Dict, Optional
from pyngrok import ngrok
from src.infrastructure.settings.logger import configurar_logging_ngrok
from src.infrastructure.settings.config import ajustes
from src.infrastructure.settings.logger import AppLogger
from src.application.ports.servicio_tunel import ServicioTunel

class NgrokGateway(ServicioTunel):
    def iniciar(self, logger: AppLogger) -> Optional[str]:
        if not ajustes.usar_ngrok:
            return None
        configurar_logging_ngrok(logger)
        try:
            if ajustes.ngrok_auth_token:
                ngrok.set_auth_token(ajustes.ngrok_auth_token)
            
            # --- MEJORA: Verificar si ya existe un túnel para este puerto ---
            tunnels = ngrok.get_tunnels()
            for tunnel in tunnels:
                # Comparamos la dirección configurada del túnel existente
                if tunnel.config.get('addr') == f"localhost:{ajustes.app_port}":
                    logger.info(f"Reutilizando túnel existente: {tunnel.public_url}")
                    return tunnel.public_url

            # --- Si no existe, crear uno nuevo ---
            opciones: Dict[str, Any] = {}
            if ajustes.ngrok_domain:
                opciones["domain"] = ajustes.ngrok_domain
            
            public_url = ngrok.connect(str(ajustes.app_port), **opciones).public_url
            logger.info(f"Túnel ngrok abierto en: {public_url}")
            return public_url
        except Exception as e:
            logger.error(f"Error al iniciar el túnel de ngrok: {e}")
            return None
