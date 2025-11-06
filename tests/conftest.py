"""
Configuração de Fixtures do Pytest

Este arquivo contém fixtures compartilhadas entre todos os testes.
Fixtures são funções que fornecem dados ou configurações reutilizáveis
para múltiplos testes, promovendo o princípio DRY (Don't Repeat Yourself).
"""

import pytest
from fastapi.testclient import TestClient
from main import app

# Credenciais para login no sistema
# Estas credenciais devem corresponder a um usuário admin existente no banco
# IMPORTANTE: Ajuste estas credenciais conforme seu banco de dados de desenvolvimento
LOGIN_EMAIL = "admin@example.com"  # Ajuste conforme necessário
LOGIN_PASSWORD = "admin123"  # Ajuste conforme necessário


@pytest.fixture(scope="module")
def client():
    """
    Fixture que fornece um TestClient do FastAPI.
    
    O TestClient permite simular requisições HTTP sem iniciar um servidor real,
    tornando os testes mais rápidos e isolados.
    
    Scope "module": criado uma vez por arquivo de teste, reutilizado em todos os testes.
    """
    return TestClient(app)


@pytest.fixture(scope="module")
def client_and_token(client):
    """
    Fixture que fornece um TestClient e um token JWT válido.
    
    Realiza login automaticamente e fornece o token de autenticação,
    evitando repetição de código de login em cada teste que precisa
    acessar endpoints protegidos.
    
    Returns:
        tuple: (TestClient, str) - Cliente HTTP e token de acesso
    """
    # Realiza login via API para obter token de acesso
    login_response = client.post("/auth/login", data={
        "username": LOGIN_EMAIL,
        "password": LOGIN_PASSWORD
    })
    
    # Verifica se o login foi bem-sucedido
    if login_response.status_code != 200:
        pytest.fail(
            f"Falha no login durante setup dos testes. "
            f"Verifique as credenciais em conftest.py. "
            f"Status: {login_response.status_code}, "
            f"Resposta: {login_response.text}"
        )
    
    token = login_response.json()["access_token"]
    return client, token


@pytest.fixture
def auth_headers(client_and_token):
    """
    Fixture que fornece headers de autenticação prontos para uso.
    
    Simplifica o uso em testes que precisam apenas dos headers,
    sem precisar do client completo.
    
    Returns:
        dict: Headers com Authorization Bearer token
    """
    _, token = client_and_token
    return {"Authorization": f"Bearer {token}"}
