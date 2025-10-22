# users/user_repository.py
"""
Repository Pattern: Abstrai operações CRUD do banco de dados.

Separa a lógica de acesso a dados da lógica de negócio,
fornecendo uma interface limpa para operações com User.
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from . import user_model
from .user_factory import UserFactory


class UserRepository:
    """
    Repository Pattern: Centraliza operações de persistência de User.
    
    Responsável por:
    - Abstrair queries SQL/ORM
    - Fornecer interface consistente para acesso a dados
    - Isolar a camada de dados da lógica de negócio
    """
    
    def __init__(self, db: Session):
        """
        Inicializa o repositório com uma sessão do banco.
        
        Args:
            db: Sessão ativa do banco de dados
        """
        self.db = db
    
    # --- OPERAÇÕES DE LEITURA (READ) ---
    
    def get_by_id(self, user_id: int) -> Optional[user_model.User]:
        """
        Busca um usuário pelo ID.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            User ou None se não encontrado
        """
        return self.db.query(user_model.User).filter(
            user_model.User.id == user_id
        ).first()
    
    def get_by_email(self, email: str) -> Optional[user_model.User]:
        """
        Busca um usuário pelo email.
        
        Args:
            email: Email do usuário
            
        Returns:
            User ou None se não encontrado
        """
        return self.db.query(user_model.User).filter(
            user_model.User.email == email.lower()
        ).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[user_model.User]:
        """
        Lista todos os usuários com paginação.
        
        Args:
            skip: Número de registros para pular
            limit: Número máximo de registros a retornar
            
        Returns:
            Lista de usuários
        """
        return self.db.query(user_model.User).offset(skip).limit(limit).all()
    
    def exists_by_email(self, email: str) -> bool:
        """
        Verifica se existe um usuário com o email informado.
        
        Args:
            email: Email a verificar
            
        Returns:
            True se existe, False caso contrário
        """
        return self.db.query(user_model.User).filter(
            user_model.User.email == email.lower()
        ).first() is not None
    
    # --- OPERAÇÃO DE CRIAÇÃO (CREATE) ---
    
    def create(self, user: user_model.UserCreate, role_id: int) -> user_model.User:
        """
        Cria um novo usuário no banco de dados.
        
        Utiliza o UserFactory para criar a entidade.
        
        Args:
            user: Schema Pydantic com dados do usuário
            role_id: ID do role associado
            
        Returns:
            User criado com ID gerado
        """
        # Utiliza o Factory Pattern para criar a entidade
        db_user = UserFactory.create_from_schema(user, role_id)
        
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
    
    # --- OPERAÇÃO DE ATUALIZAÇÃO (UPDATE) ---
    
    def update(self, db_user: user_model.User, user_in: user_model.UserUpdate) -> user_model.User:
        """
        Atualiza os dados de um usuário existente.
        
        Utiliza o UserFactory para processar a atualização.
        
        Args:
            db_user: Instância existente do User
            user_in: Schema Pydantic com dados para atualização
            
        Returns:
            User atualizado
        """
        # Utiliza o Factory Pattern para processar a atualização
        updated_user = UserFactory.update_user_entity(db_user, user_in)
        
        self.db.add(updated_user)
        self.db.commit()
        self.db.refresh(updated_user)
        return updated_user
    
    # --- OPERAÇÃO DE DELEÇÃO (DELETE) ---
    
    def delete(self, db_user: user_model.User) -> None:
        """
        Remove um usuário do banco de dados.
        
        Args:
            db_user: Instância do User a ser removida
        """
        self.db.delete(db_user)
        self.db.commit()


# ==================================
# FUNÇÕES DE COMPATIBILIDADE
# ==================================
# Mantém compatibilidade com código existente

def get_user(db: Session, user_id: int) -> Optional[user_model.User]:
    """Função de compatibilidade - usa o repositório internamente."""
    repo = UserRepository(db)
    return repo.get_by_id(user_id)


def get_user_by_email(db: Session, email: str) -> Optional[user_model.User]:
    """Função de compatibilidade - usa o repositório internamente."""
    repo = UserRepository(db)
    return repo.get_by_email(email)


def get_users(db: Session) -> List[user_model.User]:
    """Função de compatibilidade - usa o repositório internamente."""
    repo = UserRepository(db)
    return repo.get_all()


def create_user(db: Session, user: user_model.UserCreate, role_id: int) -> user_model.User:
    """Função de compatibilidade - usa o repositório internamente."""
    repo = UserRepository(db)
    return repo.create(user, role_id)


def update_user(db: Session, db_user: user_model.User, user_in: user_model.UserUpdate) -> user_model.User:
    """Função de compatibilidade - usa o repositório internamente."""
    repo = UserRepository(db)
    return repo.update(db_user, user_in)


def delete_user(db: Session, db_user: user_model.User) -> None:
    """Função de compatibilidade - usa o repositório internamente."""
    repo = UserRepository(db)
    repo.delete(db_user)
