# Especificación de Requisitos de Software (SRS)

## 1. Introducción
El puente Rasa-Chatwoot es un componente de middleware diseñado para permitir interacciones automatizadas dentro de una conversación de Chatwoot, utilizando Rasa como motor de diálogo.

## 2. Requisitos funcionales
### 2.1 Webhook Listener
- El puente debe recibir webhooks `message_created` de Chatwoot.
- Debe transformar el payload al formato REST de Rasa.
### 2.2 Integración Rasa
- Enviar mensajes al endpoint `/webhooks/rest/webhook`.
### 2.3 Respuesta a Chatwoot
- Recibir respuesta de Rasa y reenviar a Chatwoot vía API (`POST /api/v1/.../messages`).

## 3. Requisitos no funcionales
- **Escalabilidad:** Operación *stateless* para permitir escalado horizontal.
- **Rendimiento:** Latencia mínima en la transformación de payloads.
- **Mantenibilidad:** Arquitectura desacoplada (*Clean Architecture*).

## 4. Configuración
Variables necesarias: `CHATWOOT_BASE_URL`, `CHATWOOT_API_TOKEN`, `RASA_URL`.