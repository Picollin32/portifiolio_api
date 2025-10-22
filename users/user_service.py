# users/user_service.py
"""
Service Layer: Camada de lógica de negócio para Users.

Responsável por:
- Implementar regras de negócio
- Orquestrar operações entre repositórios
- Validar dados antes de persistir
- Tratar exceções e fornecer respostas adequadas
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from . import user_repository, user_model
from .user_factory import UserValidator


class UserService:
    """
    Service Layer: Encapsula a lógica de negócio relacionada a Users.
    
    Esta classe segue o padrão de camada de serviço, separando
    a lógica de negócio da camada de apresentação (controllers)
    e da camada de dados (repositories).
    """
    
    def __init__(self, db: Session):
        """
        Inicializa o serviço com uma sessão do banco.
        
        Args:
            db: Sessão ativa do banco de dados
        """
        self.db = db
        self.repository = user_repository.UserRepository(db)
    
    def create_user(self, user: user_model.UserCreate) -> user_model.User:
        """
        Cria um novo usuário com validações de negócio.
        
        Regras de negócio:
        - Email deve ser único
        - Role deve existir
        - Senha deve atender requisitos mínimos
        
        Args:
            user: Dados do usuário a ser criado
            
        Returns:
            User criado
            
        Raises:
            HTTPException: Se email já estiver em uso ou role não existir
        """
        # Validação: Email único
        UserValidator.validate_unique_email(self.db, user.email)
        
        # Validação: Role existe
        UserValidator.validate_role_exists(self.db, user.role_id)
        
        # Cria o usuário através do repositório
        return self.repository.create(user, user.role_id)
    
    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[user_model.User]:
        """
        Lista todos os usuários com paginação.
        
        Args:
            skip: Número de registros para pular
            limit: Número máximo de registros
            
        Returns:
            Lista de usuários
        """
        return self.repository.get_all(skip=skip, limit=limit)
    
    def get_user_by_id(self, user_id: int) -> user_model.User:
        """
        Busca um usuário pelo ID.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            User encontrado
            
        Raises:
            HTTPException: Se usuário não for encontrado
        """
        db_user = self.repository.get_by_id(user_id)
        
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário com ID {user_id} não encontrado"
            )
        
        return db_user
    
    def get_user_by_email(self, email: str) -> user_model.User:
        """
        Busca um usuário pelo email.
        
        Args:
            email: Email do usuário
            
        Returns:
            User encontrado
            
        Raises:
            HTTPException: Se usuário não for encontrado
        """
        db_user = self.repository.get_by_email(email)
        
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuário com email {email} não encontrado"
            )
        
        return db_user
    
    def update_user(self, user_id: int, user_in: user_model.UserUpdate) -> user_model.User:
        """
        Atualiza os dados de um usuário.
        
        Regras de negócio:
        - Usuário deve existir
        - Email deve ser único (se alterado)
        
        Args:
            user_id: ID do usuário a atualizar
            user_in: Dados para atualização
            
        Returns:
            User atualizado
            
        Raises:
            HTTPException: Se usuário não existir ou email já estiver em uso
        """
        # Busca o usuário existente
        db_user = self.get_user_by_id(user_id)
        
        # Se o email está sendo alterado, valida unicidade
        if user_in.email and user_in.email != db_user.email:
            UserValidator.validate_unique_email(
                self.db, 
                user_in.email, 
                exclude_user_id=user_id
            )
        
        # Atualiza através do repositório
        return self.repository.update(db_user, user_in)
    
    def delete_user(self, user_id: int) -> None:
        """
        Remove um usuário do sistema.
        
        Args:
            user_id: ID do usuário a remover
            
        Raises:
            HTTPException: Se usuário não for encontrado
        """
        # Busca o usuário existente
        db_user = self.get_user_by_id(user_id)
        
        # Remove através do repositório
        self.repository.delete(db_user)
    
    def reset_user_password(self, user_id: int, new_password: str) -> user_model.User:
        """
        Redefine a senha de um usuário (operação administrativa).
        
        Args:
            user_id: ID do usuário
            new_password: Nova senha
            
        Returns:
            User com senha atualizada
            
        Raises:
            HTTPException: Se usuário não existir
        """
        # Busca o usuário existente
        db_user = self.get_user_by_id(user_id)
        
        # Cria um objeto de atualização apenas com a senha
        user_update = user_model.UserUpdate(password=new_password)
        
        # Atualiza através do repositório
        return self.repository.update(db_user, user_update)


# ==================================
# FUNÇÕES DE COMPATIBILIDADE
# ==================================
# Mantém compatibilidade com código existente

def create_new_user(db: Session, user: user_model.UserCreate) -> user_model.User:
    """Função de compatibilidade - usa o serviço internamente."""
    service = UserService(db)
    return service.create_user(user)


def get_all_users(db: Session) -> List[user_model.User]:
    """Função de compatibilidade - usa o serviço internamente."""
    service = UserService(db)
    return service.get_all_users()


def get_user_by_id(db: Session, user_id: int) -> user_model.User:
    """Função de compatibilidade - usa o serviço internamente."""
    service = UserService(db)
    return service.get_user_by_id(user_id)


def update_existing_user(db: Session, user_id: int, user_in: user_model.UserUpdate) -> user_model.User:
    """Função de compatibilidade - usa o serviço internamente."""
    service = UserService(db)
    return service.update_user(user_id, user_in)


def delete_user_by_id(db: Session, user_id: int) -> None:
    """Função de compatibilidade - usa o serviço internamente."""
    service = UserService(db)
    service.delete_user(user_id)


def reset_user_password(db: Session, user_id: int, new_password: str) -> user_model.User:
    """Função de compatibilidade - usa o serviço internamente."""
    service = UserService(db)
    return service.reset_user_password(user_id, new_password)