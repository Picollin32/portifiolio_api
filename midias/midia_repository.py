# midias/midia_repository.py

from sqlalchemy.orm import Session
from . import midia_model

# --- FUNÇÕES DE LEITURA (READ) ---
def get_midia(db: Session, midia_id: int):
    """
    Busca um único usuário pelo seu ID.
    db.query(midia_model.Midia): Inicia uma consulta na tabela Midia.
    .filter(midia_model.Midia.id == midia_id): Filtra os resultados onde o id seja igual ao fornecido.
    .first(): Retorna o primeiro resultado encontrado ou None se não encontrar.
    """
    return db.query(midia_model.Midia).filter(midia_model.Midia.id == midia_id).first()

def get_midia_by_email(db: Session, email: str):
    """Busca um único usuário pelo seu e-mail."""
    return db.query(midia_model.Midia).filter(midia_model.Midia.email == email).first()

def get_midias(db: Session):
    """
    Busca todos os usuários cadastrados no banco de dados.
    .all(): Retorna uma lista com todos os resultados da consulta.
    """
    return db.query(midia_model.Midia).all()

# --- FUNÇÃO DE CRIAÇÃO (CREATE) ---
def create_midia(db: Session, midia: midia_model.MidiaCreate):
    """
    Cria um novo usuário no banco de dados.
    """
    # AVISO: A senha aqui ainda não está segura! Veremos como fazer o hash na próxima aula.
    hashed_password = midia.password

    # Cria uma instância do modelo SQLAlchemy com os dados do schema Pydantic.
    # É aqui que os dados da API são transformados em um objeto que pode ser salvo no banco.
    db_midia = midia_model.Midia(email=midia.email, hashed_password=hashed_password, full_name=midia.full_name)

    db.add(db_midia)      # Adiciona o novo objeto à sessão (área de preparação).
    db.commit()         # Salva (commita) as mudanças no banco de dados.
    db.refresh(db_midia) # Atualiza o objeto db_midia com os dados do banco (como o ID gerado).
    return db_midia

# --- FUNÇÃO DE ATUALIZAÇÃO (UPDATE) ---
def update_midia(db: Session, db_midia: midia_model.Midia, midia_in: midia_model.MidiaUpdate):
    """Atualiza os dados de um usuário existente."""
    update_data = midia_in.model_dump(exclude_unset=True) # Pega só os campos que foram enviados na requisição.
    for key, value in update_data.items():
         # Se o campo for 'password', precisa mapear para 'hashed_password' no modelo SQLAlchemy
        if key == "password":
            setattr(db_midia, "hashed_password", value) # AVISO: A senha ainda não está sendo hasheada!
        else:
            setattr(db_midia, key, value) # Atualiza cada campo no objeto do banco (db_midia).

    db.add(db_midia) # Adiciona o objeto modificado à sessão.
    db.commit()     # Salva as alterações.
    db.refresh(db_midia) # Atualiza o objeto com os dados do banco.
    return db_midia

# --- FUNÇÃO DE DELEÇÃO (DELETE) ---
def delete_midia(db: Session, db_midia: midia_model.Midia):
    """Deleta um usuário do banco de dados."""
    db.delete(db_midia) # Marca o objeto para deleção.
    db.commit()        # Efetiva a deleção no banco.
    return db_midia