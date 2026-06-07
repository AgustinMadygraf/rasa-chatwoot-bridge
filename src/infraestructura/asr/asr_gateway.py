# Path: src/infraestructura/asr/asr_gateway.py

import os
import tempfile
import time
import asyncio
from faster_whisper import WhisperModel
from src.aplicacion.puertos.puerta_enlace_asr import PuertaEnlaceASR
from src.aplicacion.puertos.cliente_http import ClienteHTTP
from src.infraestructura.settings.registrador import logger
from src.aplicacion.excepciones import ErrorDescargaAudio, ErrorInferenciaASR

class WhisperASRGateway(PuertaEnlaceASR):
    def __init__(self, cliente_http: ClienteHTTP, api_token: str):
        self.cliente_http = cliente_http
        self.api_token = api_token
        # Carga el modelo en memoria
        self.model = WhisperModel("base", device="cpu", compute_type="int8")

    async def transcribir_audio(self, audio_url: str) -> str:
        start_time = time.time()
        cabeceras = {"api_access_token": self.api_token}
        
        try:
            respuesta = await self.cliente_http.obtener(audio_url, cabeceras=cabeceras)
        except Exception as e:
            logger.registrar_error(f"Error de red descargando audio: {str(e)}")
            raise ErrorDescargaAudio("Fallo de conexión al descargar el audio")
        
        if respuesta.codigo_estado != 200:
            logger.registrar_error(f"Error HTTP {respuesta.codigo_estado} descargando audio")
            raise ErrorDescargaAudio(f"Error HTTP al descargar: {respuesta.codigo_estado}")
            
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp.write(respuesta.contenido_binario)
            tmp_path = tmp.name
            
        try:
            # Ejecutar inferencia en un hilo separado para no bloquear el event loop
            # Se fuerza el idioma a español para mejorar precisión
            segments, _ = await asyncio.to_thread(self.model.transcribe, tmp_path, language="es")
            
            transcripciones = []
            for segment in segments:
                transcripciones.append(str(segment.text))
                
            texto = " ".join(transcripciones)
            
            duration = time.time() - start_time
            logger.informar(f"Transcripción exitosa en {duration:.2f} segundos")
            return texto
        except Exception as e:
            logger.registrar_error(f"Error en inferencia ASR: {str(e)}")
            raise ErrorInferenciaASR(f"Fallo en la transcripción: {str(e)}")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
