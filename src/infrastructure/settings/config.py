"""
Path: src/infrastructure/settings/config.py
"""

import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Configuracion:
    chatwoot_base_url: str = os.getenv("CHATWOOT_BASE_URL", "")
    chatwoot_api_token: str = os.getenv("CHATWOOT_API_TOKEN", "")
    chatwoot_account_id: str = os.getenv("CHATWOOT_ACCOUNT_ID", "1")
    rasa_url: str = os.getenv("RASA_URL", "")

    usar_ngrok: bool = os.getenv("USE_NGROK", "False").lower() == "true"
    ngrok_auth_token: str = os.getenv("NGROK_AUTH_TOKEN", "")
    app_port: int = int(os.getenv("PORT", "8000"))

ajustes = Configuracion()
