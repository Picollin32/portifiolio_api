# midias/midia_model.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, Field
from database import Base # Importa a Base que criamos

# ==================================
# MODELO DA TABELA (SQLAlchemy)
# ==================================
# Esta classe define a estrutura da tabela 'midias' no banco de dados.
class Midia(Base):
    __tablename__ = "midias"  # Nome da tabela no banco

    # Colunas da tabela
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True, nullable=False)  # Título da mídia
    tipo = Column(String, nullable=False)  # Tipo: Jogo, Filme, Série, Livro, etc.
    genero = Column(String, nullable=True)  # Gênero: Action/Adventure, RPG, etc.
    ano = Column(Integer, nullable=True)  # Ano de lançamento
    status = Column(String, nullable=True)  # Status: Zerado, Em andamento, Pausado, etc.
    avaliacao = Column(Float, nullable=True)  # Avaliação de 0 a 5
    capa = Column(String, nullable=True)  # Caminho ou URL da imagem de capa
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # Proprietário da mídia
    
    # Relacionamento com User
    user = relationship("User", lazy="joined")

# ==================================
# SCHEMAS (Pydantic) - O CONTRATO DA API
# ==================================
# Estes schemas definem como os dados são recebidos e enviados pela API.

# Schema para os dados que o cliente envia ao CRIAR uma mídia
class MidiaCreate(BaseModel):
    titulo: str = Field(min_length=1)  # Título obrigatório
    tipo: str = Field(min_length=1)  # Tipo obrigatório (Jogo, Filme, Série, etc.)
    genero: str | None = None  # Gênero opcional
    ano: int | None = Field(default=None, ge=1800, le=2100)  # Ano entre 1800 e 2100
    status: str | None = None  # Status opcional (Zerado, Em andamento, etc.)
    avaliacao: float | None = Field(default=None, ge=0, le=5)  # Avaliação de 0 a 5
    capa: str | None = None  # Caminho ou URL da imagem de capa

# Schema para os dados que o cliente envia ao ATUALIZAR uma mídia
class MidiaUpdate(BaseModel):
    titulo: str | None = Field(default=None, min_length=1)
    tipo: str | None = Field(default=None, min_length=1)
    genero: str | None = None
    ano: int | None = Field(default=None, ge=1800, le=2100)
    status: str | None = None
    avaliacao: float | None = Field(default=None, ge=0, le=5)
    capa: str | None = None

# Schema para os dados que a API RETORNA ao cliente (público)
class MidiaPublic(BaseModel):
    id: int
    titulo: str
    tipo: str
    genero: str | None = None
    ano: int | None = None
    status: str | None = None
    avaliacao: float | None = None
    capa: str | None = None
    user_id: int  # ID do proprietário da mídia