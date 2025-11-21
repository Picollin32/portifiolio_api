# midias/midia_controller.py
"""
Presentation Layer (Controller): Endpoints da API para Midias.

Responsável por:
- Receber requisições HTTP
- Validar entrada (via Pydantic)
- Delegar lógica de negócio para a camada de serviço
- Retornar respostas HTTP adequadas
"""

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, Query
from typing import List, Optional, Dict
from database import get_db
from . import midia_service, midia_model
from auth.dependencies import get_current_user, get_current_admin_user
from users.user_model import User
from midias_config import get_tipos_midia, get_status_por_tipo, get_generos_por_tipo

router = APIRouter(prefix="/midias", tags=["Midias"])


# ========================================
# Endpoints de Configuração (Públicos)
# IMPORTANTE: Devem vir ANTES dos endpoints com path parameters
# ========================================

@router.get(
    "/config",
    response_model=Dict,
    summary="Obter toda a configuração de mídias",
    description="Retorna um dicionário com tipos, status e gêneros disponíveis."
)
def get_config() -> Dict:
    """
    Retorna toda a configuração de mídias de uma vez.
    
    Útil para popular formulários e dropdowns no frontend.
    
    Retorna:
    ```json
    {
        "tipos": ["Jogo", "Filme", ...],
        "status_por_tipo": {
            "Jogo": ["Zerado", "Platinado", ...],
            "Filme": ["Assistido", ...]
        },
        "generos_por_tipo": {
            "Jogo": ["Action/Adventure", "RPG", ...],
            "Filme": ["Ação", "Drama", ...]
        }
    }
    ```
    """
    from midias_config import TIPOS_MIDIA, STATUS_POR_TIPO, GENEROS_COMUNS
    
    return {
        "tipos": TIPOS_MIDIA,
        "status_por_tipo": STATUS_POR_TIPO,
        "generos_por_tipo": GENEROS_COMUNS
    }


@router.get(
    "/tipos",
    response_model=List[str],
    summary="Listar tipos de mídia disponíveis",
    description="Retorna lista de todos os tipos de mídia suportados pelo sistema."
)
def get_tipos() -> List[str]:
    """
    Lista todos os tipos de mídia disponíveis.
    
    Tipos suportados: Jogo, Filme, Série, Livro, Anime, Mangá, HQ/Comic, Podcast
    """
    return get_tipos_midia()


@router.get(
    "/status/{tipo}",
    response_model=List[str],
    summary="Listar status disponíveis por tipo",
    description="Retorna lista de status sugeridos para um tipo específico de mídia."
)
def get_status_options(tipo: str) -> List[str]:
    """
    Lista os status disponíveis para um tipo de mídia.
    
    - **tipo**: Tipo da mídia (Jogo, Filme, Série, etc.)
    
    Retorna lista de status sugeridos ou lista vazia se o tipo não for encontrado.
    """
    return get_status_por_tipo(tipo)


@router.get(
    "/generos/{tipo}",
    response_model=List[str],
    summary="Listar gêneros comuns por tipo",
    description="Retorna lista de gêneros comuns para um tipo específico de mídia."
)
def get_generos_options(tipo: str) -> List[str]:
    """
    Lista os gêneros comuns para um tipo de mídia.
    
    - **tipo**: Tipo da mídia (Jogo, Filme, Série, etc.)
    
    Retorna lista de gêneros comuns ou lista vazia se o tipo não for encontrado.
    """
    return get_generos_por_tipo(tipo)


# ========================================
# Endpoints CRUD de Mídias (Autenticados)
# ========================================

@router.post(
    "/",
    response_model=midia_model.MidiaPublic,
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova mídia",
    description="Endpoint para cadastrar uma nova mídia (jogo, filme, série, livro, etc.) no portfólio."
)
def create_midia(
    midia: midia_model.MidiaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> midia_model.MidiaPublic:
    """
    Cria uma nova mídia no sistema associada ao usuário autenticado.
    
    - **titulo**: Título da mídia
    - **tipo**: Tipo (Jogo, Filme, Série, Livro, etc.)
    - **genero**: Gênero (opcional)
    - **ano**: Ano de lançamento (opcional)
    - **status**: Status (Zerado, Em andamento, etc.) (opcional)
    - **avaliacao**: Avaliação de 0 a 5 (opcional)
    - **capa**: Caminho ou URL da imagem de capa (opcional)
    """
    return midia_service.create_new_midia(db=db, midia=midia, user_id=current_user.id)


@router.get(
    "/",
    response_model=List[midia_model.MidiaPublic],
    summary="Listar todas as mídias",
    description="Retorna lista de mídias do usuário autenticado (ou todas se for admin), com filtros opcionais."
)
def read_midias(
    tipo: Optional[str] = Query(None, description="Filtrar por tipo (Jogo, Filme, Série, etc.)"),
    status_filter: Optional[str] = Query(None, alias="status", description="Filtrar por status (Zerado, Em andamento, etc.)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> List[midia_model.MidiaPublic]:
    """
    Lista as mídias do sistema.
    
    **Regras de acesso:**
    - Usuários comuns: veem apenas suas próprias mídias
    - Admin: vê todas as mídias cadastradas
    
    **Filtros opcionais**:
    - tipo: Filtrar por tipo de mídia
    - status: Filtrar por status
    """
    # Determina se deve filtrar por user_id (None = admin vê tudo)
    user_id_filter = None if current_user.role.name == "admin" else current_user.id
    
    if tipo:
        return midia_service.get_midias_by_tipo(db, tipo=tipo, user_id=user_id_filter)
    elif status_filter:
        return midia_service.get_midias_by_status(db, status=status_filter, user_id=user_id_filter)
    else:
        return midia_service.get_all_midias(db, user_id=user_id_filter)


@router.get(
    "/{midia_id}",
    response_model=midia_model.MidiaPublic,
    summary="Buscar mídia por ID",
    description="Retorna os dados de uma mídia específica (se pertencer ao usuário ou se for admin)."
)
def read_midia(
    midia_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> midia_model.MidiaPublic:
    """
    Busca uma mídia pelo ID.
    
    **Regras de acesso:**
    - Usuários comuns: podem ver apenas suas próprias mídias
    - Admin: pode ver qualquer mídia
    
    - **midia_id**: ID da mídia a buscar
    """
    # Determina se deve filtrar por user_id
    user_id_filter = None if current_user.role.name == "admin" else current_user.id
    return midia_service.get_midia_by_id(db, midia_id=midia_id, user_id=user_id_filter)


@router.put(
    "/{midia_id}",
    response_model=midia_model.MidiaPublic,
    summary="Atualizar mídia",
    description="Atualiza os dados de uma mídia existente (se pertencer ao usuário)."
)
def update_midia(
    midia_id: int,
    midia: midia_model.MidiaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> midia_model.MidiaPublic:
    """
    Atualiza os dados de uma mídia.
    
    **Regras de acesso:**
    - Usuários podem atualizar apenas suas próprias mídias
    - Admin pode atualizar qualquer mídia
    
    - **midia_id**: ID da mídia a atualizar
    - Todos os campos são opcionais
    """
    # Usuários comuns só podem editar suas próprias mídias
    user_id_filter = current_user.id if current_user.role.name != "admin" else None
    
    # Se não for admin, verifica a propriedade durante a atualização
    if current_user.role.name != "admin":
        return midia_service.update_existing_midia(db=db, midia_id=midia_id, midia_in=midia, user_id=current_user.id)
    else:
        # Admin pode atualizar sem verificar propriedade, mas precisa buscar primeiro
        db_midia = midia_service.get_midia_by_id(db, midia_id=midia_id, user_id=None)
        return midia_service.update_existing_midia(db=db, midia_id=midia_id, midia_in=midia, user_id=db_midia.user_id)


@router.delete(
    "/{midia_id}",
    response_model=midia_model.MidiaPublic,
    summary="Deletar mídia",
    description="Remove uma mídia do sistema (se pertencer ao usuário ou se for admin)."
)
def delete_midia(
    midia_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> midia_model.MidiaPublic:
    """
    Remove uma mídia do sistema.
    
    **Regras de acesso:**
    - Usuários podem deletar apenas suas próprias mídias
    - Admin pode deletar qualquer mídia
    
    - **midia_id**: ID da mídia a remover
    
    Retorna os dados da mídia removida.
    """
    # Determina se deve filtrar por user_id
    user_id_filter = None if current_user.role.name == "admin" else current_user.id
    
    # Primeiro busca a mídia para retornar os dados antes de deletar
    db_midia = midia_service.get_midia_by_id(db, midia_id=midia_id, user_id=user_id_filter)
    
    # Cria uma cópia dos dados para retornar
    midia_data = midia_model.MidiaPublic(
        id=db_midia.id,
        titulo=db_midia.titulo,
        tipo=db_midia.tipo,
        genero=db_midia.genero,
        ano=db_midia.ano,
        status=db_midia.status,
        avaliacao=db_midia.avaliacao,
        capa=db_midia.capa,
        user_id=db_midia.user_id
    )
    
    # Agora deleta a mídia (usando o user_id correto para validação)
    delete_user_id = current_user.id if current_user.role.name != "admin" else db_midia.user_id
    midia_service.delete_midia_by_id(db=db, midia_id=midia_id, user_id=delete_user_id)
    
    # Retorna os dados salvos
    return midia_data
