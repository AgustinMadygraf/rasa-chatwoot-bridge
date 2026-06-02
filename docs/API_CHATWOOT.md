# API Chatwoot (Integración)

Este documento detalla los endpoints de Chatwoot utilizados por el puente.

## Webhooks Recibidos
- **Evento:** message_created
- **Método:** POST
- **Estructura clave:**
  - event: "message_created"
  - content: Contenido del mensaje.
  - message_type: "incoming" (para filtrar).
  - conversation: { id: ... }

## API Consumida (Outgoing)
- **Endpoint:** /api/v1/accounts/{account_id}/conversations/{conversation_id}/messages
- **Payload:**
  {
    "content": "string",
    "message_type": "outgoing"
  }
- **Auth:** Header api_access_token.
