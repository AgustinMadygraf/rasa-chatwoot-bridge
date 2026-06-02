# TODO List

## Fase 1: Dominio
- [ ] Definir Entidades de Dominio (`src/domain/entities/`)

## Fase 2: Infraestructura / Gateways
- [ ] Implementar `ChatwootGateway` (`src/interface_adapters/gateways/`)
- [ ] Implementar `RasaGateway` (`src/interface_adapters/gateways/`)

## Fase 3: Aplicación
- [ ] Implementar `Orchestrator` (`src/application/`)
- [ ] Implementar transformadores de payloads (`src/application/`)

## Fase 4: Controladores
- [ ] Implementar `WebhookController` (`src/interface_adapters/controllers/`)

## Fase 5: Infraestructura / Main
- [ ] Configurar FastAPI en `src/infrastructure/web/fastapi/`
- [ ] Configurar punto de entrada en `main.py`

## Fase 6: Validación
- [ ] Escribir tests unitarios y de integración (`tests/`)