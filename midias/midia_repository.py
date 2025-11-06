# midias/midia_repository.py

from sqlalchemy.orm import Session
from . import midia_model

# --- FUNÇÕES DE LEITURA (READ) ---
def get_midia(db: Session, midia_id: int):
    """
    Busca uma única mídia pelo seu ID.
    db.query(midia_model.Midia): Inicia uma consulta na tabela Midia.
    .filter(midia_model.Midia.id == midia_id): Filtra os resultados onde o id seja igual ao fornecido.
    .first(): Retorna o primeiro resultado encontrado ou None se não encontrar.
    """
    return db.query(midia_model.Midia).filter(midia_model.Midia.id == midia_id).first()

def get_midia_by_titulo(db: Session, titulo: str):
    """Busca uma única mídia pelo seu título."""
    return db.query(midia_model.Midia).filter(midia_model.Midia.titulo == titulo).first()

def get_midias(db: Session):
    """
    Busca todas as mídias cadastradas no banco de dados.
    .all(): Retorna uma lista com todos os resultados da consulta.
    """
    return db.query(midia_model.Midia).all()

def get_midias_by_tipo(db: Session, tipo: str):
    """Busca todas as mídias de um tipo específico (Jogo, Filme, Série, etc.)."""
    return db.query(midia_model.Midia).filter(midia_model.Midia.tipo == tipo).all()

def get_midias_by_status(db: Session, status: str):
    """Busca todas as mídias com um status específico (Zerado, Em andamento, etc.)."""
    return db.query(midia_model.Midia).filter(midia_model.Midia.status == status).all()

# --- FUNÇÃO DE CRIAÇÃO (CREATE) ---
def create_midia(db: Session, midia: midia_model.MidiaCreate):
    """
    Cria uma nova mídia no banco de dados.
    """
    # Cria uma instância do modelo SQLAlchemy com os dados do schema Pydantic.
    db_midia = midia_model.Midia(
        titulo=midia.titulo,
        tipo=midia.tipo,
        genero=midia.genero,
        ano=midia.ano,
        status=midia.status,
        avaliacao=midia.avaliacao,
        capa=midia.capa
    )

    db.add(db_midia)      # Adiciona o novo objeto à sessão (área de preparação).
    db.commit()         # Salva (commita) as mudanças no banco de dados.
    db.refresh(db_midia) # Atualiza o objeto db_midia com os dados do banco (como o ID gerado).
    return db_midia

# --- FUNÇÃO DE ATUALIZAÇÃO (UPDATE) ---
def update_midia(db: Session, db_midia: midia_model.Midia, midia_in: midia_model.MidiaUpdate):
    """Atualiza os dados de uma mídia existente."""
    update_data = midia_in.model_dump(exclude_unset=True) # Pega só os campos que foram enviados na requisição.
    for key, value in update_data.items():
        setattr(db_midia, key, value) # Atualiza cada campo no objeto do banco (db_midia).

    db.add(db_midia) # Adiciona o objeto modificado à sessão.
    db.commit()     # Salva as alterações.
    db.refresh(db_midia) # Atualiza o objeto com os dados do banco.
    return db_midia

# --- FUNÇÃO DE DELEÇÃO (DELETE) ---
def delete_midia(db: Session, db_midia: midia_model.Midia):
    """Deleta uma mídia do banco de dados."""
    db.delete(db_midia) # Marca o objeto para deleção.
    db.commit()        # Efetiva a deleção no banco.
    return db_midia