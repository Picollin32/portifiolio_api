# midias/midia_model.py

from sqlalchemy import Column, Integer, String
from pydantic import BaseModel, EmailStr, Field
from database import Base # Importa a Base que criamos

# ==================================
# MODELO DA TABELA (SQLAlchemy)
# ==================================
# Esta classe define a estrutura da tabela 'midias' no banco de dados.
class Midia(Base):
    __tablename__ = "midias"  # Nome da tabela no banco

    # Colunas da tabela
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True) # E-mail deve ser único
    hashed_password = Column(String) # Armazenaremos a senha "hasheada"
    full_name = Column(String, index=True, nullable=True) # Nome pode ser nulo
    image = Column(String, nullable=True)  # Campo para armazenar URL/data URI da imagem

# ==================================
# SCHEMAS (Pydantic) - O CONTRATO DA API
# ==================================
# Estes schemas definem como os dados são recebidos e enviados pela API.

# Schema para os dados que o cliente envia ao CRIAR um usuário
class MidiaCreate(BaseModel):
    email: EmailStr  # Valida o formato do e-mail
    password: str = Field(min_length=8)
    full_name: str | None = Field(default=None, min_length=3)
    image: str | None = None

# Schema para os dados que o cliente envia ao ATUALIZAR um usuário
class MidiaUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8)
    full_name: str | None = Field(default=None, min_length=3)
    image: str | None = None

# Schema para os dados que a API RETORNA ao cliente (público)
# NUNCA inclua a senha ou outros dados sensíveis aqui!
class MidiaPublic(BaseModel):
    id: int
    email: EmailStr
    full_name: str | None = None
    image: str | None = None