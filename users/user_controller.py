# users/user_controller.py
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from database import get_db
from auth.dependencies import get_current_admin_user
from . import user_service, user_model

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=user_model.UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(user: user_model.UserCreate, db: Session = Depends(get_db)):
    """Endpoint público para criar um novo usuário (registro)."""
    return user_service.create_new_user(db=db, user=user)

@router.get("/", response_model=List[user_model.UserPublic])
def read_users(
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """Endpoint para listar todos os usuários (ADMIN ONLY)."""
    return user_service.get_all_users(db)

@router.get("/{user_id}", response_model=user_model.UserPublic)
def read_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """Endpoint para buscar um usuário pelo ID (ADMIN ONLY)."""
    return user_service.get_user_by_id(db, user_id=user_id)

@router.put("/{user_id}", response_model=user_model.UserPublic)
def update_user(
    user_id: int, 
    user: user_model.UserUpdate, 
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """Endpoint para atualizar um usuário (ADMIN ONLY)."""
    return user_service.update_existing_user(db=db, user_id=user_id, user_in=user)

@router.put("/{user_id}/reset-password", response_model=user_model.UserPublic)
def reset_user_password(
    user_id: int,
    password_data: user_model.PasswordReset,
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """Endpoint para admin redefinir a senha de um usuário (ADMIN ONLY)."""
    return user_service.reset_user_password(db=db, user_id=user_id, new_password=password_data.new_password)

@router.delete("/{user_id}", response_model=user_model.UserPublic)
def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_admin = Depends(get_current_admin_user)
):
    """Endpoint para deletar um usuário (ADMIN ONLY)."""
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
