# main.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from users import user_controller
from roles import role_controller
from auth import auth_controller
from database import APP_PROFILE, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API do Meu Projeto", version="0.1.0")

# Configuração do CORS - Permite todas as origens em desenvolvimento
# Em produção, substitua ["*"] pelas URLs específicas do seu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite qualquer origem (desenvolvimento)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos os métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos os headers
)

app.include_router(user_controller.router)
app.include_router(role_controller.router)
app.include_router(auth_controller.router)
    # Configuração para produção

if APP_PROFILE == "PROG":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "https://programacaoiii-front.onrender.com",
            "https://programacaoiii-front.onrender.com/",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
else:
    # Configuração permissiva para desenvolvimento
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)