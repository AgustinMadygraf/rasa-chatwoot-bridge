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

ajustes = Configuracion()
