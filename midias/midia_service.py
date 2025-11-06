# midias/midia_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List
from . import midia_repository, midia_model

def create_new_midia(db: Session, midia: midia_model.MidiaCreate):
    """Serviço para criar uma nova mídia com regra de negócio."""
    # REGRA DE NEGÓCIO: Antes de criar, verificar se já existe uma mídia com o mesmo título.
    db_midia = midia_repository.get_midia_by_titulo(db, titulo=midia.titulo)
    if db_midia:
        # Se a mídia já existe, lança uma exceção HTTP que o FastAPI retornará ao cliente.
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Mídia com o título '{midia.titulo}' já está cadastrada"
        )

    # Se a regra passar, chama o repositório para efetivamente criar a mídia.
    return midia_repository.create_midia(db=db, midia=midia)

def get_all_midias(db: Session):
    """Serviço para listar todas as mídias. Neste caso, apenas repassa a chamada."""
    return midia_repository.get_midias(db)

def get_midias_by_tipo(db: Session, tipo: str) -> List[midia_model.Midia]:
    """Serviço para listar mídias por tipo (Jogo, Filme, Série, etc.)."""
    return midia_repository.get_midias_by_tipo(db, tipo=tipo)

def get_midias_by_status(db: Session, status: str) -> List[midia_model.Midia]:
    """Serviço para listar mídias por status (Zerado, Em andamento, etc.)."""
    return midia_repository.get_midias_by_status(db, status=status)

def get_midia_by_id(db: Session, midia_id: int):
    """Serviço para buscar uma mídia pelo ID, com tratamento de erro."""
    db_midia = midia_repository.get_midia(db, midia_id=midia_id)
    # REGRA DE NEGÓCIO: Se a mídia não for encontrada, retornar um erro 404.
    if db_midia is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Mídia com ID {midia_id} não encontrada"
        )
    return db_midia

def update_existing_midia(db: Session, midia_id: int, midia_in: midia_model.MidiaUpdate):
    """Serviço para atualizar uma mídia, com tratamento de erro."""
    db_midia = get_midia_by_id(db, midia_id) # Reutiliza a lógica para buscar e checar se a mídia existe.
    
    # Se o título está sendo alterado, verifica se já existe outra mídia com esse título
    if midia_in.titulo and midia_in.titulo != db_midia.titulo:
        existing_midia = midia_repository.get_midia_by_titulo(db, titulo=midia_in.titulo)
        if existing_midia:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Já existe outra mídia com o título '{midia_in.titulo}'"
            )
    
    return midia_repository.update_midia(db=db, db_midia=db_midia, midia_in=midia_in)

def delete_midia_by_id(db: Session, midia_id: int):
    """Serviço para deletar uma mídia, com tratamento de erro."""
    db_midia = get_midia_by_id(db, midia_id) # Reutiliza a lógica para buscar e checar se a mídia existe.
    return midia_repository.delete_midia(db=db, db_midia=db_midia)