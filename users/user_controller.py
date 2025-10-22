# users/user_controller.py
"""
Presentation Layer (Controller): Endpoints da API para Users.

Responsável por:
- Receber requisições HTTP
- Validar entrada (via Pydantic)
- Delegar lógica de negócio para a camada de serviço
- Retornar respostas HTTP adequadas
"""

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from database import get_db
from auth.dependencies import get_current_admin_user
from . import user_service, user_model

router = APIRouter(prefix="/users", tags=["Users"])


@router.post(
    "/",
    response_model=user_model.UserPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo usuário",
    description="Endpoint público para registro de novos usuários no sistema."
)
def create_user(
    user: user_model.UserCreate,
    db: Session = Depends(get_db)
) -> user_model.UserPublic:
    """
    Cria um novo usuário no sistema.
    
    - **email**: Email único do usuário
    - **password**: Senha (mínimo 8 caracteres)
    - **full_name**: Nome completo (opcional)
    - **profile_image_url**: URL da foto de perfil (opcional)
    - **role_id**: ID do perfil/role do usuário
    """
    return user_service.create_new_user(db=db, user=user)


@router.get(
    "/",
    response_model=List[user_model.UserPublic],
    summary="Listar todos os usuários",
    description="Retorna lista de todos os usuários cadastrados. Requer permissão de administrador."
)
def read_users(
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
) -> List[user_model.UserPublic]:
    """
    Lista todos os usuários do sistema.
    
    **Permissão necessária**: Administrador
    """
    return user_service.get_all_users(db)


@router.get(
    "/{user_id}",
    response_model=user_model.UserPublic,
    summary="Buscar usuário por ID",
    description="Retorna os dados de um usuário específico. Requer permissão de administrador."
)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
) -> user_model.UserPublic:
    """
    Busca um usuário pelo ID.
    
    - **user_id**: ID do usuário a buscar
    
    **Permissão necessária**: Administrador
    """
    return user_service.get_user_by_id(db, user_id=user_id)


@router.put(
    "/{user_id}",
    response_model=user_model.UserPublic,
    summary="Atualizar usuário",
    description="Atualiza os dados de um usuário existente. Requer permissão de administrador."
)
def update_user(
    user_id: int,
    user: user_model.UserUpdate,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
) -> user_model.UserPublic:
    """
    Atualiza os dados de um usuário.
    
    - **user_id**: ID do usuário a atualizar
    - **full_name**: Novo nome (opcional)
    - **profile_image_url**: Nova URL de imagem (opcional)
    - **password**: Nova senha (opcional)
    
    **Permissão necessária**: Administrador
    """
    return user_service.update_existing_user(db=db, user_id=user_id, user_in=user)


@router.put(
    "/{user_id}/reset-password",
    response_model=user_model.UserPublic,
    summary="Redefinir senha de usuário",
    description="Permite que administradores redefinam a senha de um usuário."
)
def reset_user_password(
    user_id: int,
    password_data: user_model.PasswordReset,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
) -> user_model.UserPublic:
    """
    Redefine a senha de um usuário (operação administrativa).
    
    - **user_id**: ID do usuário
    - **new_password**: Nova senha (mínimo 8 caracteres)
    
    **Permissão necessária**: Administrador
    """
    return user_service.reset_user_password(
        db=db,
        user_id=user_id,
        new_password=password_data.new_password
    )


@router.delete(
    "/{user_id}",
    response_model=user_model.UserPublic,
    summary="Deletar usuário",
    description="Remove um usuário do sistema. Requer permissão de administrador."
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
) -> user_model.UserPublic:
    """
    Remove um usuário do sistema.
    
    - **user_id**: ID do usuário a remover
    
    **Permissão necessária**: Administrador
    
    Retorna os dados do usuário removido.
    """
    # Primeiro busca o usuário para retornar os dados antes de deletar
    db_user = user_service.get_user_by_id(db, user_id=user_id)
    
    # Cria uma cópia dos dados para retornar
    user_data = user_model.UserPublic(
        id=db_user.id,
        email=db_user.email,
        full_name=db_user.full_name,
        profile_image_url=db_user.profile_image_url,
        role=db_user.role
    )
    
    # Agora deleta o usuário
    user_service.delete_user_by_id(db=db, user_id=user_id)
    
    # Retorna os dados salvos
    return user_data
