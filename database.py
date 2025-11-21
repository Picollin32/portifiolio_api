# database.py
"""
Módulo de gerenciamento de banco de dados com padrão Singleton.
Garante uma única instância de conexão com o PostgreSQL.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from typing import Generator
import os


class DatabaseManager:
    """
    Singleton Pattern: Garante uma única instância de conexão com o banco de dados.
    
    Esta classe gerencia a conexão com PostgreSQL, criando apenas uma engine
    e uma fábrica de sessões durante todo o ciclo de vida da aplicação.
    """
    
    _instance = None
    _engine = None
    _session_local = None
    _base = None
    
    def __new__(cls):
        """Implementação do padrão Singleton."""
        if cls._instance is None:
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Inicializa a conexão com o banco de dados (executado apenas uma vez)."""
        if self._engine is None:
            # Determina a URL do banco baseado no perfil da aplicação
            app_profile = os.getenv("APP_PROFILE", "DEV")
            
            if app_profile == "DEV":
                database_url = "postgresql://postgres:123456@localhost/portfolio_db"
                connect_args = {}
            else:
                database_url = os.getenv("DATABASE_URL")
                # Render fornece URL com postgres://, mas SQLAlchemy exige postgresql://
                if database_url.startswith("postgres://"):
                    database_url = database_url.replace("postgres://", "postgresql://", 1)
                
                # Configuração SSL necessária para Render PostgreSQL
                connect_args = {
                    "sslmode": "require"
                }
            
            # Cria a engine do SQLAlchemy (ponto de entrada para o banco)
            self._engine = create_engine(
                database_url,
                pool_pre_ping=True,  # Verifica conexões antes de usar
                pool_size=5,         # Número de conexões no pool
                max_overflow=10,     # Conexões extras permitidas
                connect_args=connect_args  # Parâmetros SSL para produção
            )
            
            # Cria a fábrica de sessões
            self._session_local = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine
            )
            
            # Cria a classe Base para os modelos ORM
            self._base = declarative_base()
    
    @property
    def engine(self):
        """Retorna a engine do banco de dados."""
        return self._engine
    
    @property
    def session_local(self):
        """Retorna a fábrica de sessões."""
        return self._session_local
    
    @property
    def base(self):
        """Retorna a classe Base para modelos ORM."""
        return self._base
    
    def get_session(self) -> Generator[Session, None, None]:
        """
        Dependency Injection: Fornece uma sessão do banco de dados.
        
        Garante que a sessão seja sempre fechada após o uso,
        mesmo em caso de exceções.
        
        Yields:
            Session: Sessão ativa do banco de dados
        """
        session = self._session_local()
        try:
            yield session
        finally:
            session.close()
    
    def create_all_tables(self):
        """Cria todas as tabelas definidas nos modelos."""
        self._base.metadata.create_all(bind=self._engine)


# ==================================
# INSTÂNCIA GLOBAL (Singleton)
# ==================================
db_manager = DatabaseManager()

# ==================================
# EXPORTS PARA COMPATIBILIDADE
# ==================================
# Mantém compatibilidade com código existente
APP_PROFILE = os.getenv("APP_PROFILE", "DEV")
engine = db_manager.engine
SessionLocal = db_manager.session_local
Base = db_manager.base


def get_db() -> Generator[Session, None, None]:
    """
    Função de dependência para injeção de sessão do banco.
    
    Utiliza o DatabaseManager Singleton para fornecer sessões.
    Esta função é usada como dependência nos endpoints FastAPI.
    
    Yields:
        Session: Sessão ativa do banco de dados
    """
    yield from db_manager.get_session()
