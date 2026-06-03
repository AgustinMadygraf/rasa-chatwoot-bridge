"""
Path: src/application/exceptions.py
"""

class AplicacionError(Exception):
    """Clase base para errores de la capa de aplicación."""
    pass

class AccesoNoAutorizadoError(AplicacionError):
    """Error lanzado cuando el token de validación es inválido."""
    pass

class ErrorProcesamientoWebhook(AplicacionError):
    """Error lanzado cuando ocurre un fallo al procesar el mensaje."""
    pass
