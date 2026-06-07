# Guía del Proyecto (GEMINI.md)

## Estándares de Arquitectura
- El proyecto sigue estrictamente **Clean Architecture**.
- Estructura de carpetas:
  - `src/dominio/`: Entidades y modelos de dominio.
  - `src/application/`: Casos de uso y orquestación.
  - `src/interface_adapters/`: Adaptadores (Gateways, Controllers, Presenters).
  - `src/infrastructure/`: Detalles técnicos (FastAPI, clientes HTTP).

## Convenciones
- **Idioma:** Todo el código, documentación y mensajes deben estar en español.
- **Testing:** Todo cambio en la lógica de negocio debe incluir su test correspondiente en `tests/`.
- **Framework:** FastAPI.
- **Estilo:** Código limpio, tipado fuerte y modularidad.