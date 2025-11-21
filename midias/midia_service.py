# midias/midia_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from . import midia_repository, midia_model

def create_new_midia(db: Session, midia: midia_model.MidiaCreate, user_id: int):
    """Serviço para criar uma nova mídia com regra de negócio."""
    # REGRA DE NEGÓCIO: Antes de criar, verificar se já existe uma mídia com o mesmo título para este usuário.
    db_midia = midia_repository.get_midia_by_titulo(db, titulo=midia.titulo, user_id=user_id)
    if db_midia:
        # Se a mídia já existe para este usuário, lança uma exceção HTTP que o FastAPI retornará ao cliente.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Você já possui uma mídia cadastrada com o título '{midia.titulo}'"
        )

    # Se a regra passar, chama o repositório para efetivamente criar a mídia.
    return midia_repository.create_midia(db=db, midia=midia, user_id=user_id)

def get_all_midias(db: Session, user_id: Optional[int] = None):
    """Serviço para listar todas as mídias. Se user_id for None, retorna todas (admin)."""
    return midia_repository.get_midias(db, user_id=user_id)

def get_midias_by_tipo(db: Session, tipo: str, user_id: Optional[int] = None) -> List[midia_model.Midia]:
    """Serviço para listar mídias por tipo, filtrando por usuário se fornecido."""
    return midia_repository.get_midias_by_tipo(db, tipo=tipo, user_id=user_id)

def get_midias_by_status(db: Session, status: str, user_id: Optional[int] = None) -> List[midia_model.Midia]:
    """Serviço para listar mídias por status, filtrando por usuário se fornecido."""
    return midia_repository.get_midias_by_status(db, status=status, user_id=user_id)

def get_midia_by_id(db: Session, midia_id: int, user_id: Optional[int] = None):
    """Serviço para buscar uma mídia pelo ID, com tratamento de erro e verificação de propriedade."""
    db_midia = midia_repository.get_midia(db, midia_id=midia_id, user_id=user_id)
    # REGRA DE NEGÓCIO: Se a mídia não for encontrada ou não pertence ao usuário, retornar um erro 404.
    if db_midia is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Mídia com ID {midia_id} não encontrada"
        )
    return db_midia

def update_existing_midia(db: Session, midia_id: int, midia_in: midia_model.MidiaUpdate, user_id: int):
    """Serviço para atualizar uma mídia, com tratamento de erro e verificação de propriedade."""
    # Busca a mídia e verifica se pertence ao usuário
    db_midia = get_midia_by_id(db, midia_id, user_id=user_id)
    
    # Se o título está sendo alterado, verifica se já existe outra mídia com esse título para este usuário
    if midia_in.titulo and midia_in.titulo != db_midia.titulo:
        existing_midia = midia_repository.get_midia_by_titulo(db, titulo=midia_in.titulo, user_id=user_id)
        if existing_midia:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Você já possui outra mídia cadastrada com o título '{midia_in.titulo}'"
            )
    
    return midia_repository.update_midia(db=db, db_midia=db_midia, midia_in=midia_in)

def delete_midia_by_id(db: Session, midia_id: int, user_id: int):
    """Serviço para deletar uma mídia, com tratamento de erro e verificação de propriedade."""
    # Busca a mídia e verifica se pertence ao usuário
    db_midia = get_midia_by_id(db, midia_id, user_id=user_id)
    return midia_repository.delete_midia(db=db, db_midia=db_midia)