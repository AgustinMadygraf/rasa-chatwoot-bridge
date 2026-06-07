# Path: src/aplicacion/excepciones.py

class AplicacionError(Exception):
    pass

class AccesoNoAutorizadoError(AplicacionError):
    pass

class ErrorProcesamientoWebhook(AplicacionError):
    pass
