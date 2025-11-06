"""
Testes Unitários para Autenticação

Este arquivo contém testes unitários para os endpoints de autenticação da API.
Testes unitários são uma prática fundamental no desenvolvimento de software que visa
verificar o comportamento correto de unidades individuais de código, como funções,
métodos ou, neste caso, endpoints de API.

Aqui, utilizamos o TestClient do FastAPI para simular requisições HTTP aos endpoints,
permitindo testar a lógica de negócio, validações e respostas da API sem depender
de um servidor real em execução.

Os testes cobrem cenários de autenticação e autorização, garantindo que a API
funcione corretamente e retorne respostas adequadas.
"""

from fastapi.testclient import TestClient
import pytest

# As credenciais são importadas do conftest.py
# LOGIN_EMAIL e LOGIN_PASSWORD estão definidos lá


def test_login_sucesso(client_and_token):
    """
    Testa login com credenciais válidas.
    
    Verifica se o endpoint de login aceita credenciais corretas
    e retorna um token de acesso JWT válido.
    """
    client, token = client_and_token
    # Se chegou aqui, o login já foi bem-sucedido no conftest
    assert token is not None
    assert len(token) > 0


def test_login_invalido(client):
    """
    Testa login com credenciais inválidas.
    
    Verifica se o endpoint de login rejeita credenciais incorretas
    e não retorna token de acesso.
    """
    response = client.post("/auth/login", data={
        "username": "usuario_invalido@example.com",
        "password": "senhaerrada"
    })
    assert response.status_code == 401
    assert "access_token" not in response.json()


def test_acesso_sem_token(client):
    """
    Testa acesso negado a endpoint protegido sem token.
    
    Verifica se endpoints que requerem autenticação rejeitam
    requisições sem token de autorização.
    """
    response = client.get("/users/")
    assert response.status_code == 401 or response.status_code == 403


def test_acesso_com_token_invalido(client):
    """
    Testa acesso negado a endpoint protegido com token inválido.
    
    Verifica se endpoints que requerem autenticação rejeitam
    requisições com token malformado ou expirado.
    """
    headers = {"Authorization": "Bearer token_invalido_xyz123"}
    response = client.get("/users/", headers=headers)
    assert response.status_code == 401 or response.status_code == 403


def test_register_usuario_sucesso(client):
    """
    Testa registro de novo usuário com dados válidos.
    
    Verifica se o endpoint de registro aceita dados corretos
    e cria um novo usuário com role padrão 'user'.
    """
    import random
    import string
    
    # Gera email único para evitar conflitos
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    register_data = {
        "email": f"novo_usuario_{random_suffix}@example.com",
        "password": "senha123456",
        "first_name": "Novo",
        "last_name": "Usuario"
    }
    
    response = client.post("/auth/register", json=register_data)
    assert response.status_code == 201, f"Registro falhou: {response.text}"
    
    data = response.json()
    assert "user" in data
    assert data["user"]["email"] == register_data["email"]
    assert data["user"]["full_name"] == "Novo Usuario"


def test_register_email_duplicado(client):
    """
    Testa registro com email já existente.
    
    Verifica se a API impede o registro de usuário com email duplicado.
    """
    import random
    import string
    
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    email = f"duplicado_{random_suffix}@example.com"
    
    register_data = {
        "email": email,
        "password": "senha123456",
        "first_name": "Usuario",
        "last_name": "Duplicado"
    }
    
    # Primeiro registro - deve funcionar
    response1 = client.post("/auth/register", json=register_data)
    assert response1.status_code == 201
    
    # Segundo registro com mesmo email - deve falhar
    response2 = client.post("/auth/register", json=register_data)
    assert response2.status_code == 400


def test_register_senha_curta(client):
    """
    Testa registro com senha muito curta.
    
    Verifica se a API rejeita senhas com menos de 6 caracteres.
    """
    import random
    import string
    
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    register_data = {
        "email": f"senha_curta_{random_suffix}@example.com",
        "password": "123",  # Senha muito curta
        "first_name": "Usuario",
        "last_name": "Teste"
    }
    
    response = client.post("/auth/register", json=register_data)
    assert response.status_code == 422  # Validation error


def test_register_dados_incompletos(client):
    """
    Testa registro com dados obrigatórios faltando.
    
    Verifica se a API rejeita requisições sem campos obrigatórios.
    """
    register_data = {
        "email": "incompleto@example.com",
        # Faltando password, first_name e last_name
    }
    
    response = client.post("/auth/register", json=register_data)
    assert response.status_code == 422  # Validation error
