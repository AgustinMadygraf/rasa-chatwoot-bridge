import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.infraestructura.httpx.cliente_httpx import ClienteHttpx
from src.infraestructura.pyngrok.ngrok_gateway import PasarelaNgrok
from src.infraestructura.settings.registrador import configurar_logger
from src.aplicacion.puertos.registrador import Registrador

@pytest.mark.asyncio
async def test_httpx_client_post():
    url = 'http://test.com'
    json_data = {'key': 'value'}
    cabeceras = {'Authorization': 'Bearer token'}
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'status': 'ok'}
    with patch('src.infraestructura.httpx.cliente_httpx.AsyncClient') as mock_async_client:
        mock_client_instance = mock_async_client.return_value.__aenter__.return_value
        mock_client_instance.post = AsyncMock(return_value=mock_response)
        client = ClienteHttpx()
        response = await client.enviar(url, json=json_data, cabeceras=cabeceras)
        assert response.codigo_estado == 200
        assert response.json() == {'status': 'ok'}
        mock_client_instance.post.assert_awaited_once_with(url, json=json_data, headers=cabeceras)

@patch('src.infraestructura.pyngrok.ngrok_gateway.ajustes')
@patch('src.infraestructura.pyngrok.ngrok_gateway.ngrok')
@patch('src.infraestructura.pyngrok.ngrok_gateway.configurar_logging_ngrok')
def test_ngrok_gateway_iniciar_no_usar_ngrok(mock_log, mock_ngrok, mock_ajustes):
    mock_ajustes.usar_ngrok = False
    gateway = PasarelaNgrok()
    result = gateway.iniciar(MagicMock())
    assert result is None
    mock_ngrok.connect.assert_not_called()

@patch('src.infraestructura.pyngrok.ngrok_gateway.ajustes')
@patch('src.infraestructura.pyngrok.ngrok_gateway.ngrok')
@patch('src.infraestructura.pyngrok.ngrok_gateway.configurar_logging_ngrok')
def test_ngrok_gateway_iniciar_exitoso(mock_log, mock_ngrok, mock_ajustes):
    mock_ajustes.usar_ngrok = True
    mock_ajustes.puerto_aplicacion = 8000
    mock_ajustes.token_auth_ngrok = None
    mock_ajustes.dominio_ngrok = None
    mock_ngrok.get_tunnels.return_value = []
    mock_tunnel = MagicMock()
    mock_tunnel.public_url = 'http://public.url'
    mock_ngrok.connect.return_value = mock_tunnel
    gateway = PasarelaNgrok()
    logger = MagicMock()
    result = gateway.iniciar(logger)
    assert result == 'http://public.url'
    mock_ngrok.connect.assert_called_once_with('8000')
    logger.informar.assert_called()

@patch('src.infraestructura.pyngrok.ngrok_gateway.ajustes')
@patch('src.infraestructura.pyngrok.ngrok_gateway.ngrok')
@patch('src.infraestructura.pyngrok.ngrok_gateway.configurar_logging_ngrok')
def test_ngrok_gateway_reutilizar_tunel(mock_log, mock_ngrok, mock_ajustes):
    mock_ajustes.usar_ngrok = True
    mock_ajustes.puerto_aplicacion = 8000
    mock_ajustes.dominio_ngrok = None
    mock_tunnel = MagicMock()
    mock_tunnel.config = {'addr': 'localhost:8000'}
    mock_tunnel.public_url = 'http://reused.url'
    mock_ngrok.get_tunnels.return_value = [mock_tunnel]
    gateway = PasarelaNgrok()
    logger = MagicMock()
    result = gateway.iniciar(logger)
    assert result == 'http://reused.url'
    logger.informar.assert_called_with('Reutilizando túnel existente: http://reused.url')

@patch('src.infraestructura.pyngrok.ngrok_gateway.ajustes')
@patch('src.infraestructura.pyngrok.ngrok_gateway.ngrok')
@patch('src.infraestructura.pyngrok.ngrok_gateway.configurar_logging_ngrok')
def test_ngrok_gateway_registrar_error(mock_log, mock_ngrok, mock_ajustes):
    mock_ajustes.usar_ngrok = True
    mock_ngrok.get_tunnels.side_effect = Exception('NGROK ERROR')
    gateway = PasarelaNgrok()
    logger = MagicMock()
    result = gateway.iniciar(logger)
    assert result is None
    logger.registrar_error.assert_called()

def test_configurar_logger():
    logger = configurar_logger()
    assert isinstance(logger, Registrador)
