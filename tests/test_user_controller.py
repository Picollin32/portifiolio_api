"""
Testes Unitários para Usuários

Este arquivo contém testes unitários para os endpoints de usuários da API.
Testes unitários são uma prática fundamental no desenvolvimento de software que visa
verificar o comportamento correto de unidades individuais de código, como funções,
métodos ou, neste caso, endpoints de API.

Aqui, utilizamos o TestClient do FastAPI para simular requisições HTTP aos endpoints,
permitindo testar a lógica de negócio, validações e respostas da API sem depender
de um servidor real em execução.

Os testes cobrem operações CRUD (Create, Read, Update, Delete) e validações de dados,
garantindo que a API funcione corretamente e retorne respostas adequadas.
"""

import random
import string


def test_user_crud_sequence(client_and_token):
    """
    Testa a sequência completa de operações CRUD para usuários.
    
    Este teste verifica se é possível criar, alterar e excluir um usuário
    através da API, validando que cada operação retorna o status correto
    e os dados esperados. Também testa a integridade dos relacionamentos
    (como a vinculação com roles).
    """
    client, token = client_and_token
    headers = {"Authorization": f"Bearer {token}"}

    # Gerar sufixo aleatório para e-mail do usuário de teste
    # Isso evita conflitos de duplicidade de e-mail entre execuções de teste
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    test_email = f"test_sequence_user_{random_suffix}@example.com"

    # Buscar uma role existente para vincular ao usuário
    # Garante que sempre haverá uma role válida para o teste,
    # evitando dependências externas ou falhas por falta de dados
    roles_resp = client.get("/roles/", headers=headers)
    assert roles_resp.status_code == 200 and len(roles_resp.json()) > 0, \
        "Nenhuma role disponível para vincular ao usuário."
    role_id = roles_resp.json()[0]["id"]

    # 1. Criar usuário
    # Testa a criação de um novo usuário com dados válidos
    user_data = {
        "email": test_email,
        "password": "password123",
        "full_name": "Test Sequence User",
        "role_id": role_id
    }
    # Chama o endpoint de criação de usuário
    user_resp = client.post("/users/", json=user_data, headers=headers)
    assert user_resp.status_code == 201, f"Falha ao criar usuário: {user_resp.text}"
    
    user_id = user_resp.json()["id"]
    user_json = user_resp.json()
    
    # Valida que os dados retornados correspondem aos enviados
    assert user_json["email"] == test_email
    assert user_json["full_name"] == "Test Sequence User"
    assert "role" in user_json and user_json["role"]["id"] == role_id

    # 2. Alterar usuário
    # Testa a atualização de dados do usuário criado
    update_user_data = {
        "full_name": "Test Sequence User Updated"
    }
    # Chama o endpoint de atualização de usuário
    update_user_resp = client.put(f"/users/{user_id}", json=update_user_data, headers=headers)
    assert update_user_resp.status_code == 200, f"Falha ao atualizar usuário: {update_user_resp.text}"
    
    update_json = update_user_resp.json()
    
    # Valida que o nome foi atualizado, mas o e-mail permanece o mesmo
    assert update_json["email"] == test_email
    assert update_json["full_name"] == "Test Sequence User Updated"
    assert "role" in update_json and update_json["role"]["id"] == role_id

    # 3. Excluir usuário
    # Testa a exclusão do usuário criado
    # Chama o endpoint de exclusão de usuário
    delete_user_resp = client.delete(f"/users/{user_id}", headers=headers)
    assert delete_user_resp.status_code == 200, f"Falha ao excluir usuário: {delete_user_resp.text}"
    
    deleted_json = delete_user_resp.json()
    
    # Valida que os dados retornados correspondem ao usuário excluído
    assert deleted_json["id"] == user_id
    assert deleted_json["email"] == test_email
    assert deleted_json["full_name"] == "Test Sequence User Updated"
    assert "role" in deleted_json and deleted_json["role"]["id"] == role_id


def test_user_listar_todos(client_and_token):
    """
    Testa a listagem de todos os usuários.
    
    Verifica se o endpoint retorna uma lista de usuários e se
    cada usuário contém os campos esperados.
    """
    client, token = client_and_token
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/users/", headers=headers)
    assert response.status_code == 200
    
    users = response.json()
    assert isinstance(users, list)
    
    if len(users) > 0:
        # Valida estrutura do primeiro usuário
        user = users[0]
        assert "id" in user
        assert "email" in user
        assert "role" in user


def test_user_buscar_por_id(client_and_token):
    """
    Testa a busca de usuário específico por ID.
    
    Cria um usuário, busca por ID e valida os dados retornados.
    """
    client, token = client_and_token
    headers = {"Authorization": f"Bearer {token}"}
    
    # Criar usuário para teste
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    # Buscar role
    roles_resp = client.get("/roles/", headers=headers)
    role_id = roles_resp.json()[0]["id"]
    
    user_data = {
        "email": f"test_busca_{random_suffix}@example.com",
        "password": "password123",
        "full_name": "Test Busca User",
        "role_id": role_id
    }
    
    create_resp = client.post("/users/", json=user_data, headers=headers)
    user_id = create_resp.json()["id"]
    
    # Buscar por ID
    response = client.get(f"/users/{user_id}", headers=headers)
    assert response.status_code == 200
    
    user = response.json()
    assert user["id"] == user_id
    assert user["email"] == user_data["email"]
    assert user["full_name"] == user_data["full_name"]
    
    # Limpar
    client.delete(f"/users/{user_id}", headers=headers)


def test_user_buscar_id_inexistente(client_and_token):
    """
    Testa busca de usuário com ID inexistente.
    
    Verifica se a API retorna erro 404 ao buscar usuário que não existe.
    """
    client, token = client_and_token
    headers = {"Authorization": f"Bearer {token}"}
    
    # Usar ID muito alto que provavelmente não existe
    response = client.get("/users/999999", headers=headers)
    assert response.status_code == 404


def test_user_email_duplicado(client_and_token):
    """
    Testa criação de usuário com email duplicado.
    
    Verifica se a API impede a criação de usuários com emails já cadastrados.
    """
    client, token = client_and_token
    headers = {"Authorization": f"Bearer {token}"}
    
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    email = f"test_duplicado_{random_suffix}@example.com"
    
    # Buscar role
    roles_resp = client.get("/roles/", headers=headers)
    role_id = roles_resp.json()[0]["id"]
    
    user_data = {
        "email": email,
        "password": "password123",
        "full_name": "Test Duplicado",
        "role_id": role_id
    }
    
    # Primeiro usuário - deve funcionar
    resp1 = client.post("/users/", json=user_data, headers=headers)
    assert resp1.status_code == 201
    user_id = resp1.json()["id"]
    
    # Segundo usuário com mesmo email - deve falhar
    resp2 = client.post("/users/", json=user_data, headers=headers)
    assert resp2.status_code == 400
    
    # Limpar
    client.delete(f"/users/{user_id}", headers=headers)


def test_user_senha_curta(client_and_token):
    """
    Testa criação de usuário com senha muito curta.
    
    Verifica se a API rejeita senhas com menos de 8 caracteres.
    """
    client, token = client_and_token
    headers = {"Authorization": f"Bearer {token}"}
    
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    # Buscar role
    roles_resp = client.get("/roles/", headers=headers)
    role_id = roles_resp.json()[0]["id"]
    
    user_data = {
        "email": f"test_senha_{random_suffix}@example.com",
        "password": "123",  # Senha muito curta (< 8 caracteres)
        "full_name": "Test Senha",
        "role_id": role_id
    }
    
    response = client.post("/users/", json=user_data, headers=headers)
    assert response.status_code == 422  # Validation error


def test_user_reset_password(client_and_token):
    """
    Testa redefinição de senha de usuário.
    
    Verifica se administradores podem redefinir a senha de um usuário.
    """
    client, token = client_and_token
    headers = {"Authorization": f"Bearer {token}"}
    
    # Criar usuário
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    roles_resp = client.get("/roles/", headers=headers)
    role_id = roles_resp.json()[0]["id"]
    
    user_data = {
        "email": f"test_reset_{random_suffix}@example.com",
        "password": "password123",
        "full_name": "Test Reset",
        "role_id": role_id
    }
    
    create_resp = client.post("/users/", json=user_data, headers=headers)
    user_id = create_resp.json()["id"]
    
    # Reset password
    reset_data = {"new_password": "newpassword123"}
    response = client.put(f"/users/{user_id}/reset-password", json=reset_data, headers=headers)
    assert response.status_code == 200
    
    # Limpar
    client.delete(f"/users/{user_id}", headers=headers)


def test_user_delete_inexistente(client_and_token):
    """
    Testa exclusão de usuário inexistente.
    
    Verifica se a API retorna erro 404 ao tentar excluir usuário que não existe.
    """
    client, token = client_and_token
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.delete("/users/999999", headers=headers)
    assert response.status_code == 404
