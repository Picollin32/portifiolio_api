# midias/midia_controller.py

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status
from typing import List
from database import SessionLocal
from . import midia_service, midia_model

router = APIRouter(prefix="/midias", tags=["Midias"])

# Esta função é a nossa "Injeção de Dependência".
# O FastAPI vai chamá-la para cada requisição que precisar de uma sessão com o banco.
# A palavra 'yield' entrega a sessão para a rota e, quando a rota termina,
# o código após o 'yield' (db.close()) é executado, garantindo que a conexão seja fechada.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=midia_model.MidiaPublic, status_code=status.HTTP_201_CREATED)
def create_midia(midia: midia_model.MidiaCreate, db: Session = Depends(get_db)):
    """Endpoint para criar um novo usuário. Recebe os dados validados (midia)
    e a sessão do banco (db) através da injeção de dependência."""
    return midia_service.create_new_midia(db=db, midia=midia)

@router.get("/", response_model=List[midia_model.MidiaPublic])
def read_midias(db: Session = Depends(get_db)):
    """Endpoint para listar todos os usuários."""
    return midia_service.get_all_midias(db)

@router.get("/{midia_id}", response_model=midia_model.MidiaPublic)
def read_midia(midia_id: int, db: Session = Depends(get_db)):
    """Endpoint para buscar um usuário pelo ID."""
    return midia_service.get_midia_by_id(db, midia_id=midia_id)

@router.put("/{midia_id}", response_model=midia_model.MidiaPublic)
def update_midia(midia_id: int, midia: midia_model.MidiaUpdate, db: Session = Depends(get_db)):
    """Endpoint para atualizar um usuário."""
    return midia_service.update_existing_midia(db=db, midia_id=midia_id, midia_in=midia)

@router.delete("/{midia_id}", response_model=midia_model.MidiaPublic)
def delete_midia(midia_id: int, db: Session = Depends(get_db)):
    """Endpoint para deletar um usuário."""
    return midia_service.delete_midia_by_id(db=db, midia_id=midia_id)
