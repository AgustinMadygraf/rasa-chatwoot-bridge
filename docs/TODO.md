# TODO List

## Fase 1: Dominio
- [x] Definir Entidades de Dominio (src/domain/entities/)

## Fase 2: Infraestructura / Gateways
- [x] Definir interfaces ChatwootGateway y RasaGateway (src/interface_adapters/gateways/)
- [x] Implementar ChatwootGateway (src/infrastructure/gateways/chatwoot_gateway.py)
- [x] Implementar RasaGateway (src/infrastructure/gateways/rasa_gateway.py)

## Fase 3: Aplicación
- [x] Implementar Orchestrator (src/application/)
- [x] Implementar transformadores de payloads (src/application/)

## Fase 4: Controladores
- [x] Implementar WebhookController (src/interface_adapters/controllers/)

## Fase 5: Infraestructura / Main
- [x] Configurar FastAPI en src/infrastructure/web/fastapi/
- [x] Configurar punto de entrada en main.py

## Fase 6: Validación
- [x] Escribir tests unitarios y de integración (tests/)
