"""
Script para popular a tabela de mídias com dados de exemplo.

Este script adiciona algumas mídias de exemplo ao banco de dados.
"""

from sqlalchemy.orm import Session
from database import SessionLocal
from midias.midia_model import Midia

def seed_midias():
    """
    Adiciona mídias de exemplo ao banco de dados.
    """
    db: Session = SessionLocal()
    
    try:
        print("🌱 Populando tabela de mídias com dados de exemplo...")
        
        # Mídias mockadas do frontend (dados originais)
        midias_exemplo = [
            Midia(
                titulo="The Last of Us Part II",
                tipo="Jogo",
                genero="Action/Adventure",
                ano=2020,
                status="Platinado",
                avaliacao=5.0,
                capa="assets/images/the-last-of-us-part-ii-game-cover.png"
            ),
            Midia(
                titulo="Dune",
                tipo="Filme",
                genero="Sci-Fi",
                ano=2021,
                status="Assistido",
                avaliacao=4.0,
                capa="assets/images/dune-movie-poster.png"
            ),
            Midia(
                titulo="Breaking Bad",
                tipo="Série",
                genero="Drama/Crime",
                ano=2008,
                status="Finalizada",
                avaliacao=5.0,
                capa="assets/images/breaking-bad-series-poster.png"
            ),
            Midia(
                titulo="God of War",
                tipo="Jogo",
                genero="Action/Adventure",
                ano=2018,
                status="Zerado",
                avaliacao=5.0,
                capa="assets/images/god-of-war-cover.png"
            ),
            Midia(
                titulo="Inception",
                tipo="Filme",
                genero="Sci-Fi/Thriller",
                ano=2010,
                status="Assistido",
                avaliacao=5.0,
                capa="assets/images/inception-inspired-poster.png"
            ),
            Midia(
                titulo="Stranger Things",
                tipo="Série",
                genero="Sci-Fi/Horror",
                ano=2016,
                status="Finalizada",
                avaliacao=4.0,
                capa="assets/images/stranger-things-series-poster.png"
            )
        ]
        
        # Adiciona todas as mídias
        for midia in midias_exemplo:
            db.add(midia)
            print(f"   ✓ Adicionado: {midia.titulo} ({midia.tipo})")
        
        db.commit()
        print(f"\n✅ {len(midias_exemplo)} mídias adicionadas com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao popular dados: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_midias()
