# Path: src/aplicacion/puertos/puerta_enlace_asr.py

from abc import ABC, abstractmethod

class PuertaEnlaceASR(ABC):
    @abstractmethod
    async def transcribir_audio(self, audio_url: str) -> str:
        pass
