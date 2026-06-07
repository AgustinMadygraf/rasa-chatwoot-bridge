# Path: src/dominio/objetos_valor.py

from dataclasses import dataclass

@dataclass(frozen=True)
class IdConversacion:
    valor: str

    def __post_init__(self):
        if not self.valor or not self.valor.strip():
            raise ValueError("El ID de conversación no puede estar vacío.")

@dataclass(frozen=True)
class IdRemitente:
    valor: str

    def __post_init__(self):
        if not self.valor or not self.valor.strip():
            raise ValueError("El ID de remitente no puede estar vacío.")
