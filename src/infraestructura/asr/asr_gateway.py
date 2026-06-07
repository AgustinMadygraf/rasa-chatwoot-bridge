# Path: src/infraestructura/asr/asr_gateway.py

from src.aplicacion.puertos.puerta_enlace_asr import PuertaEnlaceASR

class PasarelaASRMock(PuertaEnlaceASR):
    async def transcribir_audio(self, audio_url: str) -> str:
        return "texto transcrito del audio"
