"""
Testes Unitários para Roles (Perfis)

Este arquivo contém testes unitários para os endpoints de roles da API.
Testes de roles são importantes para garantir o correto funcionamento
do sistema de permissões e controle de acesso da aplicação.

Os testes cobrem operações CRUD completas e validações de dados específicas
para roles, como nomes únicos e validação de campos obrigatórios.
"""

import random
import string


def test_role_crud_sequence(client_and_token):
    """
    Testa a sequência completa de operações CRUD para roles.
    
    Verifica se é possível criar, alterar e excluir uma role através da API,
    validando status codes e dados retornados. Usa nomes aleatórios para
    evitar conflitos entre execuções de teste.
    """
    client, token = client_and_token
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Criar uma role nova
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    role_name = f"test_role_sequence_{random_suffix}"
    role_data = {"name": role_name}
    
    role_resp = client.post("/roles/", json=role_data, headers=headers)
    assert role_resp.status_code == 201, f"Falha ao criar role: {role_resp.text}"
    
    role_id = role_resp.json()["id"]
    assert role_resp.json()["name"] == role_name

    # 2. Alterar a role criada
    update_role_data = {"name": f"test_role_sequence_updated_{random_suffix}"}
    update_role_resp = client.put(f"/roles/{role_id}", json=update_role_data, headers=headers)
    assert update_role_resp.status_code == 200, f"Falha ao atualizar role: {update_role_resp.text}"
    assert update_role_resp.json()["name"] == f"test_role_sequence_updated_{random_suffix}"

    # 3. Excluir a role criada
    delete_role_resp = client.delete(f"/roles/{role_id}", headers=headers)
    assert delete_role_resp.status_code == 200, f"Falha ao excluir role: {delete_role_resp.text}"
    
    deleted_role_json = delete_role_resp.json()
    assert deleted_role_json["id"] == role_id
    assert deleted_role_json["name"] == f"test_role_sequence_updated_{random_suffix}"


def test_role_listar_todos(client_and_token):
    """
    Testa a listagem de todas as roles.
    
    Verifica se o endpoint retorna uma lista de roles e se
    cada role contém os campos esperados.
    """
    client, token = client_and_token
    headers = {"Authorization": f"Bearer {token}"}
    
    response = client.get("/roles/", headers=headers)
    assert response.status_code == 200
    
    roles = response.json()
    assert isinstance(roles, list)
    assert len(roles) > 0, "Deve haver pelo menos uma role cadastrada"
    
    # Valida estrutura da primeira role
    role = roles[0]
    assert "id" in role
    assert "name" in role


def test_role_nome_ausente(client_and_token):
    """
    Testa criação de role sem nome (campo obrigatório).
    
    Verifica se a API rejeita corretamente a criação quando o campo
    obrigatório 'name' não é fornecido, retornando erro de validação.
    """
    client, token = client_and_token
    headers = {"Authorization": f"Bearer {token}"}
    
    role_data = {}
    resp = client.post("/roles/", json=role_data, headers=headers)
    assert resp.status_code == 422, f"Role criada sem nome: {resp.text}"


def test_role_nome_duplicado(client_and_token):
    """
    Testa criação de role com nome duplicado.
    
    Cria uma role, tenta criar outra com o mesmo nome e verifica
    se a API impede a duplicidade. Limpa os dados após o teste.
    """
    client, token = client_and_token
    headers = {"Authorization": f"Bearer {token}"}
    
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    role_name = f"role_duplicada_teste_{random_suffix}"
    role_data = {"name": role_name}
    
    # Cria a primeira role
    resp1 = client.post("/roles/", json=role_data, headers=headers)
    assert resp1.status_code == 201
    role_id = resp1.json()["id"]
    
    # Tenta criar novamente
    resp2 = client.post("/roles/", json=role_data, headers=headers)
    assert resp2.status_code == 400 or resp2.status_code == 409, \
        f"Role duplicada criada: {resp2.text}"
    
    # Limpa a role criada
    client.delete(f"/roles/{role_id}", headers=headers)


def test_role_criar_e_buscar(client_and_token):
    """
    Testa criação e busca de role específica.
    
    Cria uma role e verifica se ela aparece na listagem.
    """
    client, token = client_and_token
    headers = {"Authorization": f"Bearer {token}"}
    
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    role_name = f"test_role_busca_{random_suffix}"
    role_data = {"name": role_name}
    
    # Criar role
    create_resp = client.post("/roles/", json=role_data, headers=headers)
    assert create_resp.status_code == 201
    role_id = create_resp.json()["id"]
    
    # Buscar na listagem
    list_resp = client.get("/roles/", headers=headers)
    assert list_resp.status_code == 200
    
    roles = list_resp.json()
    role_encontrada = next((r for r in roles if r["id"] == role_id), None)
    assert role_encontrada is not None, "Role criada não encontrada na listagem"
    assert role_encontrada["name"] == role_name
    
    # Limpar
    client.delete(f"/roles/{role_id}", headers=headers)


def test_role_update_nome_vazio(client_and_token):
    """
    Testa atualização de role com nome vazio.
    
    Verifica se a API rejeita tentativas de atualizar uma role
    deixando o nome vazio.
    """
    client, token = client_and_token
    headers = {"Authorization": f"Bearer {token}"}
    
    # Criar role
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    role_name = f"test_role_update_{random_suffix}"
    role_data = {"name": role_name}
    
    create_resp = client.post("/roles/", json=role_data, headers=headers)
    role_id = create_resp.json()["id"]
    
    # Tentar atualizar com nome vazio
    update_data = {"name": ""}
    update_resp = client.put(f"/roles/{role_id}", json=update_data, headers=headers)
    assert update_resp.status_code == 422 or update_resp.status_code == 400
    
    # Limpar
    client.delete(f"/roles/{role_id}", headers=headers)


def test_role_delete_inexistente(client_and_token):
    """
    Testa exclusão de role inexistente.
    
    Verifica se a API retorna erro apropriado ao tentar excluir
    uma role que não existe.
    """
    client, token = client_and_token
    headers = {"Authorization": f"Bearer {token}"}
    
    # Tentar excluir role com ID muito alto (provavelmente inexistente)
    response = client.delete("/roles/999999", headers=headers)
    assert response.status_code == 404


def test_role_update_inexistente(client_and_token):
    """
    Testa atualização de role inexistente.
    
    Verifica se a API retorna erro apropriado ao tentar atualizar
    uma role que não existe.
    """
    client, token = client_and_token
    headers = {"Authorization": f"Bearer {token}"}
    
    update_data = {"name": "role_inexistente"}
    response = client.put("/roles/999999", json=update_data, headers=headers)
    assert response.status_code == 404


def test_role_acesso_sem_autenticacao(client):
    """
    Testa acesso aos endpoints de roles sem autenticação.
    
    Verifica se todos os endpoints de roles estão protegidos
    e rejeitam acesso não autenticado.
    """
    # Tentar listar roles sem token
    response = client.get("/roles/")
    assert response.status_code == 401 or response.status_code == 403
    
    # Tentar criar role sem token
    role_data = {"name": "test_role"}
    response = client.post("/roles/", json=role_data)
    assert response.status_code == 401 or response.status_code == 403
