"""
Script de migração para recriar a tabela de mídias com a nova estrutura.

Este script:
1. Remove a tabela antiga de mídias (se existir)
2. Cria a nova tabela com os campos corretos
"""

from database import db_manager, engine
from midias.midia_model import Midia
from sqlalchemy import inspect

def migrate_midias_table():
    """
    Recria a tabela de mídias com a nova estrutura.
    """
    print("🔄 Iniciando migração da tabela de mídias...")
    
    # Verifica se a tabela existe
    inspector = inspect(engine)
    if "midias" in inspector.get_table_names():
        print("⚠️  Tabela 'midias' existente encontrada. Será removida.")
        
        # Remove a tabela antiga
        Midia.__table__.drop(engine)
        print("✅ Tabela antiga removida.")
    
    # Cria a nova tabela
    Midia.__table__.create(engine)
    print("✅ Nova tabela de mídias criada com sucesso!")
    
    print("\n📋 Estrutura da nova tabela:")
    print("   - id: INTEGER (Primary Key)")
    print("   - titulo: STRING (obrigatório)")
    print("   - tipo: STRING (obrigatório)")
    print("   - genero: STRING (opcional)")
    print("   - ano: INTEGER (opcional)")
    print("   - status: STRING (opcional)")
    print("   - avaliacao: FLOAT (opcional, 0-5)")
    print("   - capa: STRING (opcional)")
    print("\n✨ Migração concluída!")

if __name__ == "__main__":
    migrate_midias_table()
