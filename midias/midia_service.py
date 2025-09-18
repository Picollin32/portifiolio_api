# midias/midia_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import midia_repository, midia_model

def create_new_midia(db: Session, midia: midia_model.MidiaCreate):
    """Serviço para criar um novo usuário com regra de negócio."""
    # REGRA DE NEGÓCIO: Antes de criar, verificar se o e-mail já está em uso.
    db_midia = midia_repository.get_midia_by_email(db, email=midia.email)
    if db_midia:
        # Se o usuário já existe, lança uma exceção HTTP que o FastAPI retornará ao cliente.
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Se a regra passar, chama o repositório para efetivamente criar o usuário.
    return midia_repository.create_midia(db=db, midia=midia)

def get_all_midias(db: Session):
    """Serviço para listar todos os usuários. Neste caso, apenas repassa a chamada."""
    return midia_repository.get_midias(db)

def get_midia_by_id(db: Session, midia_id: int):
    """Serviço para buscar um usuário pelo ID, com tratamento de erro."""
    db_midia = midia_repository.get_midia(db, midia_id=midia_id)
    # REGRA DE NEGÓCIO: Se o usuário não for encontrado, retornar um erro 404.
    if db_midia is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Midia not found")
    return db_midia

def update_existing_midia(db: Session, midia_id: int, midia_in: midia_model.MidiaUpdate):
    """Serviço para atualizar um usuário, com tratamento de erro."""
    db_midia = get_midia_by_id(db, midia_id) # Reutiliza a lógica para buscar e checar se o usuário existe.
    return midia_repository.update_midia(db=db, db_midia=db_midia, midia_in=midia_in)

def delete_midia_by_id(db: Session, midia_id: int):
    """Serviço para deletar um usuário, com tratamento de erro."""
    db_midia = get_midia_by_id(db, midia_id) # Reutiliza a lógica para buscar e checar se o usuário existe.
    return midia_repository.delete_midia(db=db, db_midia=db_midia)