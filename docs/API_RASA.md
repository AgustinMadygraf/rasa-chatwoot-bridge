# API Rasa (Integración)

Este documento detalla el contrato del canal REST de Rasa utilizado por el puente.

## Endpoint Consumido (Outgoing)
- **URL:** {RASA_URL}/webhooks/rest/webhook
- **Método:** POST
- **Payload:**
  {
    "sender": "conversation_id",
    "message": "user_text"
  }

## Respuesta de Rasa (Incoming al Bridge)
Rasa devuelve un array de objetos de respuesta:
[
  { "text": "Respuesta 1" },
  { "text": "Respuesta 2" }
]
