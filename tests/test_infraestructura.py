import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.infrastructure.httpx.cliente_httpx import HttpxClient
from src.infrastructure.pyngrok.ngrok_gateway import NgrokGateway
from src.infrastructure.settings.logger import configurar_logger

@pytest.mark.asyncio
async def test_httpx_client_post():
    url = 'http://test.com'
    json_data = {'key': 'value'}
    headers = {'Authorization': 'Bearer token'}
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'status': 'ok'}
    with patch('src.infrastructure.httpx.cliente_httpx.AsyncClient') as mock_async_client:
        mock_client_instance = mock_async_client.return_value.__aenter__.return_value
        mock_client_instance.post = AsyncMock(return_value=mock_response)
        client = HttpxClient()
        response = await client.post(url, json=json_data, headers=headers)
        assert response.status_code == 200
        assert response.json() == {'status': 'ok'}
        mock_client_instance.post.assert_awaited_once_with(url, json=json_data, headers=headers)

@patch('src.infrastructure.pyngrok.ngrok_gateway.ajustes')
@patch('src.infrastructure.pyngrok.ngrok_gateway.ngrok')
@patch('src.infrastructure.pyngrok.ngrok_gateway.configurar_logging_ngrok')
def test_ngrok_gateway_iniciar_no_usar_ngrok(mock_log, mock_ngrok, mock_ajustes):
    mock_ajustes.usar_ngrok = False
    gateway = NgrokGateway()
    result = gateway.iniciar(MagicMock())
    assert result is None
    mock_ngrok.connect.assert_not_called()

@patch('src.infrastructure.pyngrok.ngrok_gateway.ajustes')
@patch('src.infrastructure.pyngrok.ngrok_gateway.ngrok')
@patch('src.infrastructure.pyngrok.ngrok_gateway.configurar_logging_ngrok')
def test_ngrok_gateway_iniciar_exitoso(mock_log, mock_ngrok, mock_ajustes):
    mock_ajustes.usar_ngrok = True
    mock_ajustes.app_port = 8000
    mock_ajustes.ngrok_auth_token = None
    mock_ajustes.ngrok_domain = None
    mock_ngrok.get_tunnels.return_value = []
    mock_tunnel = MagicMock()
    mock_tunnel.public_url = 'http://public.url'
    mock_ngrok.connect.return_value = mock_tunnel
    gateway = NgrokGateway()
    logger = MagicMock()
    result = gateway.iniciar(logger)
    assert result == 'http://public.url'
    mock_ngrok.connect.assert_called_once_with('8000')
    logger.info.assert_called()

@patch('src.infrastructure.pyngrok.ngrok_gateway.ajustes')
@patch('src.infrastructure.pyngrok.ngrok_gateway.ngrok')
@patch('src.infrastructure.pyngrok.ngrok_gateway.configurar_logging_ngrok')
def test_ngrok_gateway_reutilizar_tunel(mock_log, mock_ngrok, mock_ajustes):
    mock_ajustes.usar_ngrok = True
    mock_ajustes.app_port = 8000
    mock_ajustes.ngrok_domain = None
    mock_tunnel = MagicMock()
    mock_tunnel.config = {'addr': 'localhost:8000'}
    mock_tunnel.public_url = 'http://reused.url'
    mock_ngrok.get_tunnels.return_value = [mock_tunnel]
    gateway = NgrokGateway()
    logger = MagicMock()
    result = gateway.iniciar(logger)
    assert result == 'http://reused.url'
    logger.info.assert_called_with('Reutilizando túnel existente: http://reused.url')

@patch('src.infrastructure.pyngrok.ngrok_gateway.ajustes')
@patch('src.infrastructure.pyngrok.ngrok_gateway.ngrok')
@patch('src.infrastructure.pyngrok.ngrok_gateway.configurar_logging_ngrok')
def test_ngrok_gateway_error(mock_log, mock_ngrok, mock_ajustes):
    mock_ajustes.usar_ngrok = True
    mock_ngrok.get_tunnels.side_effect = Exception('NGROK ERROR')
    gateway = NgrokGateway()
    logger = MagicMock()
    result = gateway.iniciar(logger)
    assert result is None
    logger.error.assert_called()

def test_configurar_logger():
    logger = configurar_logger()
    assert logger.name == 'puente_rasa_chatwoot'
