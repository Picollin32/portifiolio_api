# users/user_factory.py
"""
Factory Pattern para criação de objetos User.

Este módulo centraliza a lógica de criação de usuários,
incluindo validações e processamento de dados.
"""

from typing import Optional
from sqlalchemy.orm import Session
from . import user_model
from security import get_password_hash
from fastapi import HTTPException, status


class UserFactory:
    """
    Factory Pattern: Centraliza a criação de objetos User.
    
    Responsável por:
    - Validar dados de entrada
    - Processar senha (hash)
    - Criar instâncias de User com dados consistentes
    - Aplicar regras de negócio na criação
    """
    
    @staticmethod
    def create_user_entity(
        email: str,
        password: str,
        role_id: int,
        full_name: Optional[str] = None,
        profile_image_url: Optional[str] = None
    ) -> user_model.User:
        """
        Cria uma instância de User (entidade SQLAlchemy).
        
        Args:
            email: Email do usuário (único)
            password: Senha em texto plano (será hasheada)
            role_id: ID do role associado
            full_name: Nome completo (opcional)
            profile_image_url: URL da imagem de perfil (opcional)
            
        Returns:
            User: Instância do modelo User pronta para ser persistida
        """
        # Valida email
        if not email or '@' not in email:
            raise ValueError("Email inválido")
        
        # Valida senha
        if not password or len(password) < 8:
            raise ValueError("Senha deve ter no mínimo 8 caracteres")
        
        # Processa a senha (hash)
        hashed_password = get_password_hash(password)
        
        # Cria e retorna a entidade User
        return user_model.User(
            email=email.lower().strip(),  # Normaliza email
            hashed_password=hashed_password,
            full_name=full_name.strip() if full_name else None,
            profile_image_url=profile_image_url,
            role_id=role_id
        )
    
    @staticmethod
    def create_from_schema(
        user_schema: user_model.UserCreate,
        role_id: int
    ) -> user_model.User:
        """
        Cria uma instância de User a partir de um schema Pydantic.
        
        Args:
            user_schema: Schema Pydantic com dados validados
            role_id: ID do role associado
            
        Returns:
            User: Instância do modelo User
        """
        return UserFactory.create_user_entity(
            email=user_schema.email,
            password=user_schema.password,
            role_id=role_id,
            full_name=user_schema.full_name,
            profile_image_url=user_schema.profile_image_url
        )
    
    @staticmethod
    def update_user_entity(
        db_user: user_model.User,
        update_data: user_model.UserUpdate
    ) -> user_model.User:
        """
        Atualiza uma instância existente de User.
        
        Args:
            db_user: Instância existente do User
            update_data: Dados para atualização
            
        Returns:
            User: Instância atualizada
        """
        update_dict = update_data.model_dump(exclude_unset=True)
        
        for key, value in update_dict.items():
            if key == "password":
                # Processa a nova senha
                if value and len(value) >= 8:
                    db_user.hashed_password = get_password_hash(value)
            else:
                # Normaliza dados se necessário
                if key == "full_name" and value:
                    value = value.strip()
                setattr(db_user, key, value)
        
        return db_user


class UserValidator:
    """
    Classe auxiliar para validações de regras de negócio relacionadas a Users.
    """
    
    @staticmethod
    def validate_unique_email(db: Session, email: str, exclude_user_id: Optional[int] = None):
        """
        Valida se o email já está em uso.
        
        Args:
            db: Sessão do banco de dados
            email: Email a ser validado
            exclude_user_id: ID do usuário a excluir da verificação (para updates)
            
        Raises:
            HTTPException: Se o email já estiver em uso
        """
        from . import user_repository
        
        existing_user = user_repository.get_user_by_email(db, email)
        
        if existing_user and (exclude_user_id is None or existing_user.id != exclude_user_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email já está registrado"
            )
    
    @staticmethod
    def validate_role_exists(db: Session, role_id: int):
        """
        Valida se o role existe.
        
        Args:
            db: Sessão do banco de dados
            role_id: ID do role a ser validado
            
        Raises:
            HTTPException: Se o role não existir
        """
        from roles import role_repository
        
        # Busca o role por ID (você pode precisar implementar esta função)
        role = db.query(user_model.User.__table__.metadata.tables['roles']).filter_by(id=role_id).first()
        
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role com ID {role_id} não encontrado"
            )
