# Puente Rasa-Chatwoot

Middleware de alto rendimiento diseñado para conectar [Chatwoot](https://www.chatwoot.com/) y [Rasa Open Source](https://rasa.com/).

## Objetivo
Habilitar capacidades de automatización conversacional y NLU de Rasa dentro de la plataforma de soporte de Chatwoot.

## Características Principales
- **Arquitectura Limpia:** Basada en *Clean Architecture* para máxima mantenibilidad y testabilidad.
- **Bidireccional:** Comunicación fluida entre el usuario (Chatwoot) y el bot (Rasa).
- **Stateless:** Diseñado para entornos escalables.
- **Rendimiento:** Implementado con **FastAPI** para manejo asíncrono de eventos.

## Estructura del Proyecto
El proyecto sigue la organización de *Clean Architecture*:

- `src/domain/`: Modelos de negocio (Entidades).
- `src/application/`: Casos de uso y orquestación.
- `src/interface_adapters/`: Adaptadores (Controllers, Gateways).
- `src/infrastructure/`: Detalles técnicos (Framework, HTTP Clients).

## Documentación Técnica
- [Especificación de Requisitos (SRS)](docs/SRS.md)
- [Diseño de Arquitectura](docs/DESIGN.md)
- [API Chatwoot](docs/API_CHATWOOT.md)
- [API Rasa](docs/API_RASA.md)