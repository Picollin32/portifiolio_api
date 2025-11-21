"""
Script para adicionar a coluna profile_image_url na tabela users se não existir
"""
from sqlalchemy import text, inspect
from database import engine

def migrate_user_photo():
    """Adiciona a coluna profile_image_url se não existir"""
    
    with engine.connect() as conn:
        # Verifica se a coluna já existe
        inspector = inspect(engine)
        columns = [col['name'] for col in inspector.get_columns('users')]
        
        if 'profile_image_url' not in columns:
            print("Adicionando coluna profile_image_url na tabela users...")
            conn.execute(text("ALTER TABLE users ADD COLUMN profile_image_url VARCHAR"))
            conn.commit()
            print("✅ Coluna profile_image_url adicionada com sucesso!")
        else:
            print("✅ Coluna profile_image_url já existe na tabela users")

if __name__ == "__main__":
    print("🔨 Iniciando migração do banco de dados...")
    print("="*50)
    migrate_user_photo()
    print("="*50)
    print("✅ Migração concluída!")
