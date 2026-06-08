# Path: src/infrastructure/settings/config.py

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Configuracion:
    url_base_chatwoot: str = os.getenv("CHATWOOT_BASE_URL", "")
    token_api_chatwoot: str = os.getenv("CHATWOOT_API_TOKEN", "")
    id_cuenta_chatwoot: str = os.getenv("CHATWOOT_ACCOUNT_ID", "1")
    url_rasa: str = os.getenv("RASA_URL", "")
    token_webhook_chatwoot: str = os.getenv("CHATWOOT_WEBHOOK_TOKEN", "")
    usar_ngrok: bool = os.getenv("USE_NGROK", "False").lower() == "true"
    token_auth_ngrok: str = os.getenv("NGROK_AUTH_TOKEN", "")
    dominio_ngrok: str = os.getenv("NGROK_DOMAIN", "")
    puerto_aplicacion: int = int(os.getenv("PORT", "5004"))
    usar_rasa: bool = os.getenv("USE_RASA", "True").lower() == "true"
    nivel_log: str = os.getenv("LOG_LEVEL", "INFO").upper()

ajustes = Configuracion()
