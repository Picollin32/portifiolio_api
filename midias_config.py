"""
Documentação dos tipos e status de mídias suportados pelo sistema.

Este arquivo serve como referência para os valores aceitos pelos campos
'tipo' e 'status' na API de mídias.
"""

# ==================================
# TIPOS DE MÍDIA SUPORTADOS
# ==================================
"""
Os tipos de mídia são strings que identificam a categoria do item.
Valores aceitos:
"""

TIPOS_MIDIA = [
    "Jogo",
    "Filme",
    "Série",
    "Livro",
    "Anime",
    "Mangá",
    "HQ/Comic",
    "Podcast",
]

# ==================================
# STATUS POR TIPO DE MÍDIA
# ==================================
"""
Os status variam de acordo com o tipo de mídia.
Abaixo estão as sugestões de status para cada tipo:
"""

STATUS_POR_TIPO = {
    "Jogo": [
        "Zerado",
        "Platinado",
        "Em andamento",
        "Jogando",
        "Pausado",
        "Abandonado",
        "Quero jogar",
    ],
    "Filme": [
        "Assistido",
        "Favorito",
        "Para Reassistir",
        "Quero assistir",
    ],
    "Série": [
        "Finalizada",
        "Assistindo",
        "Pausada",
        "Abandonada",
        "Completa",
        "Quero assistir",
    ],
    "Livro": [
        "Lido",
        "Lendo",
        "Pausado",
        "Abandonado",
        "Quero ler",
    ],
    "Anime": [
        "Finalizado",
        "Assistindo",
        "Pausado",
        "Abandonado",
        "Completo",
        "Quero assistir",
    ],
    "Mangá": [
        "Finalizado",
        "Lendo",
        "Pausado",
        "Abandonado",
        "Completo",
        "Quero ler",
    ],
    "HQ/Comic": [
        "Finalizado",
        "Lendo",
        "Pausado",
        "Abandonado",
        "Coleção completa",
        "Quero ler",
    ],
    "Podcast": [
        "Ouvindo",
        "Pausado",
        "Completo",
        "Abandonado",
        "Quero ouvir",
    ],
}

# ==================================
# GÊNEROS COMUNS
# ==================================
"""
Exemplos de gêneros para cada tipo de mídia.
(Campo livre - aceita qualquer string)
"""

GENEROS_COMUNS = {
    "Jogo": [
        "Action/Adventure",
        "RPG",
        "FPS",
        "Souls-like",
        "Metroidvania",
        "Puzzle",
        "Estratégia",
        "Simulação",
        "Esportes",
        "Corrida",
        "Horror",
        "Indie",
    ],
    "Filme": [
        "Ação",
        "Aventura",
        "Comédia",
        "Drama",
        "Terror",
        "Suspense",
        "Sci-Fi",
        "Ficção Científica",
        "Romance",
        "Animação",
        "Documentário",
    ],
    "Série": [
        "Ação",
        "Drama",
        "Comédia",
        "Terror",
        "Suspense",
        "Sci-Fi",
        "Crime",
        "Mistério",
        "Fantasia",
        "Romance",
    ],
    "Livro": [
        "Ficção",
        "Não-ficção",
        "Ficção Científica",
        "Fantasia",
        "Terror",
        "Romance",
        "Mistério",
        "Biografia",
        "História",
        "Filosofia",
    ],
}

# ==================================
# EXEMPLO DE USO NA API
# ==================================
"""
Criar uma nova mídia:

POST /midias/
{
    "titulo": "The Last of Us Part II",
    "tipo": "Jogo",
    "genero": "Action/Adventure",
    "ano": 2020,
    "status": "Platinado",
    "avaliacao": 5.0,
    "capa": "assets/images/tlou2.png"
}

Filtrar por tipo:
GET /midias/?tipo=Jogo

Filtrar por status:
GET /midias/?status=Zerado
"""

# ==================================
# VALIDAÇÕES
# ==================================
"""
Campo       | Tipo   | Obrigatório | Validação
------------|--------|-------------|----------------------------------
titulo      | string | SIM         | Mínimo 1 caractere, único
tipo        | string | SIM         | Mínimo 1 caractere
genero      | string | NÃO         | -
ano         | int    | NÃO         | Entre 1800 e 2100
status      | string | NÃO         | -
avaliacao   | float  | NÃO         | Entre 0.0 e 5.0
capa        | string | NÃO         | Caminho ou URL da imagem
"""


def get_tipos_midia():
    """Retorna lista de tipos de mídia suportados."""
    return TIPOS_MIDIA.copy()


def get_status_por_tipo(tipo: str):
    """
    Retorna lista de status sugeridos para um tipo de mídia.
    
    Args:
        tipo: Tipo da mídia (Jogo, Filme, Série, etc.)
        
    Returns:
        Lista de status sugeridos ou lista vazia se tipo não encontrado
    """
    return STATUS_POR_TIPO.get(tipo, []).copy()


def get_generos_por_tipo(tipo: str):
    """
    Retorna lista de gêneros comuns para um tipo de mídia.
    
    Args:
        tipo: Tipo da mídia (Jogo, Filme, Série, etc.)
        
    Returns:
        Lista de gêneros comuns ou lista vazia se tipo não encontrado
    """
    return GENEROS_COMUNS.get(tipo, []).copy()


if __name__ == "__main__":
    print("📚 TIPOS DE MÍDIA SUPORTADOS:")
    print("-" * 50)
    for tipo in TIPOS_MIDIA:
        print(f"  • {tipo}")
    
    print("\n📊 STATUS POR TIPO:")
    print("-" * 50)
    for tipo, status_list in STATUS_POR_TIPO.items():
        print(f"\n{tipo}:")
        for status in status_list:
            print(f"  • {status}")
    
    print("\n🎨 GÊNEROS COMUNS:")
    print("-" * 50)
    for tipo, generos in GENEROS_COMUNS.items():
        print(f"\n{tipo}:")
        for genero in generos[:5]:  # Mostra apenas os 5 primeiros
            print(f"  • {genero}")
        if len(generos) > 5:
            print(f"  ... e mais {len(generos) - 5}")
