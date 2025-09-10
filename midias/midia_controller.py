# app/midias/controller.py
from fastapi import APIRouter, HTTPException
from fastapi import APIRouter, HTTPException, status
from .midia_model import MidiaCreate, MidiaPublic, MidiaUpdate

# 1. Cria um roteador específico para usuários
router = APIRouter(
    prefix="/midias",       # Todas as rotas aqui começarão com /midias
    tags=["Midias"]         # Agrupa as rotas no Swagger
)

# Lista FAKE para simular um banco de dados
fake_db = []

# 2. Define o endpoint para criar um usuário
@router.post("/save", response_model=MidiaPublic)
def create_midia(midia: MidiaCreate):
    # midia aqui é um objeto Pydantic, com dados já validados!
    new_midia_data = midia.model_dump()
    new_midia_data["id"] = len(fake_db) + 1

    new_midia = MidiaPublic(**new_midia_data)
    fake_db.append(new_midia)

    return new_midia 
@router.get("/", response_model=list[MidiaPublic])
def list_midias():
    # Converte os dicionários do 'banco de dados' para o modelo público
    return [MidiaPublic(**midia_data) for midia_data in fake_db.values()]

@router.put("/{midia_id}", response_model=MidiaPublic)
def update_midia(midia_id: int, midia_update: MidiaUpdate):
    if midia_id not in fake_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Midia not found")

    stored_midia_data = fake_db[midia_id]
    update_data = midia_update.model_dump(exclude_unset=True) # Apenas campos enviados

    updated_midia = stored_midia_data.copy()
    updated_midia.update(update_data)
    fake_db[midia_id] = updated_midia

    return MidiaPublic(**updated_midia)

@router.delete("/{midia_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_midia(midia_id: int):
    if midia_id not in fake_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Midia not found")

    del fake_db[midia_id]
    # Com status 204, a resposta não deve ter corpo. O FastAPI cuida disso.