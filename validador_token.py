"""
Path: validador_token.py
"""

import httpx
import asyncio
import os
from typing import Dict, Any
from dotenv import load_dotenv

# Cargar variables desde el .env del proyecto
load_dotenv()

# --- CONFIGURACIÓN ---
URL = "http://127.0.0.1:5004/webhook/chatwoot"
# Obtenemos el token automáticamente desde el entorno
TOKEN_CORRECTO: str = os.getenv("CHATWOOT_WEBHOOK_TOKEN", "")

# --- PAYLOAD DE PRUEBA COMPLETO ---
PAYLOAD_COMPLETO: Dict[str, Any] = {
    "conversation": {"id": 30},
    "content": "Hola, esto es una prueba",
    "sender": {"id": 672}
}

async def probar_token():
    async with httpx.AsyncClient() as client:
        # Prueba 3: Con token correcto y payload completo
        print(f"\nPrueba 3: Enviando con token cargado del .env...")
        resp3 = await client.post(URL, json=PAYLOAD_COMPLETO, params={"token": TOKEN_CORRECTO})
        print(f"Status (token correcto): {resp3.status_code}")
        print(f"Respuesta: {resp3.text}")

if __name__ == "__main__":
    if not TOKEN_CORRECTO:
        print("ADVERTENCIA: CHATWOOT_WEBHOOK_TOKEN no está definido en el archivo .env")
    asyncio.run(probar_token())
