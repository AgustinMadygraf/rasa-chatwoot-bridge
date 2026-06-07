# Path: src/aplicacion/excepciones.py

class AplicacionError(Exception):
    pass

class AccesoNoAutorizadoError(AplicacionError):
    pass

class ErrorProcesamientoWebhook(AplicacionError):
    pass

class ErrorInfraestructura(AplicacionError):
    pass

class ErrorDescargaAudio(ErrorInfraestructura):
    pass

class ErrorInferenciaASR(ErrorInfraestructura):
    pass
