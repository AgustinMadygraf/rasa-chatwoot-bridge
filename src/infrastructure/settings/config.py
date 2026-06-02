import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

@dataclass(frozen=True)
class Configuracion:
    chatwoot_base_url: str = os.getenv("CHATWOOT_BASE_URL", "")
    chatwoot_api_token: str = os.getenv("CHATWOOT_API_TOKEN", "")
    chatwoot_account_id: str = os.getenv("CHATWOOT_ACCOUNT_ID", "1")
    rasa_url: str = os.getenv("RASA_URL", "")
    # Token de validación para webhooks entrantes de Chatwoot
    chatwoot_webhook_token: str = os.getenv("CHATWOOT_WEBHOOK_TOKEN", "")
    
    # Configuraciones de ngrok
    usar_ngrok: bool = os.getenv("USE_NGROK", "False").lower() == "true"
    ngrok_auth_token: str = os.getenv("NGROK_AUTH_TOKEN", "")
    ngrok_domain: str = os.getenv("NGROK_DOMAIN", "")
    app_port: int = int(os.getenv("PORT", "8000"))

ajustes = Configuracion()
