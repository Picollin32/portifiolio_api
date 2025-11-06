# main.py
"""
Ponto de entrada da aplicação FastAPI.

Implementa Layered Architecture (Arquitetura em Camadas):
- Presentation Layer: Controllers (routers)
- Business Logic Layer: Services
- Data Access Layer: Repositories
- Database Layer: DatabaseManager (Singleton)
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from users import user_controller
from roles import role_controller
from auth import auth_controller
from midias import midia_controller
from database import db_manager, APP_PROFILE

# Inicializa as tabelas no banco de dados usando o Singleton DatabaseManager
db_manager.create_all_tables()

# Criação da aplicação FastAPI
app = FastAPI(
    title="Portfólio API",
    version="1.0.0",
    description="API RESTful para gerenciamento de portfólio com arquitetura em camadas",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ==================================
# CONFIGURAÇÃO DE CORS
# ==================================
if APP_PROFILE == "PROD":
    # Configuração restrita para produção
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://portifolio-front.onrender.com",
            "https://portifolio-front.onrender.com/",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
else:
    # Configuração permissiva para desenvolvimento
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Permite qualquer origem em desenvolvimento
        allow_credentials=True,
        allow_methods=["*"],  # Permite todos os métodos HTTP
        allow_headers=["*"],  # Permite todos os cabeçalhos
    )

# ==================================
# REGISTRO DE ROUTERS (Presentation Layer)
# ==================================
# Cada router representa um conjunto de endpoints relacionados
app.include_router(user_controller.router)
app.include_router(role_controller.router)
app.include_router(auth_controller.router)
app.include_router(midia_controller.router)


# ==================================
# ENDPOINT DE HEALTH CHECK
# ==================================
@app.get(
    "/health",
    tags=["Health"],
    summary="Verificação de saúde da API",
    description="Endpoint para verificar se a API está funcionando corretamente"
)
def health_check():
    """
    Verifica o status da API.
    
    Útil para monitoramento e verificação de disponibilidade.
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": APP_PROFILE
    }


# ==================================
# PONTO DE ENTRADA DA APLICAÇÃO
# ==================================
if __name__ == '__main__':
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True if APP_PROFILE == "DEV" else False
    )