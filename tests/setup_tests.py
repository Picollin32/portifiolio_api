"""
Script de Preparação para Testes

Este script cria um usuário administrador padrão no banco de dados
para ser usado durante a execução dos testes.

Execute este script antes de rodar os testes pela primeira vez.
"""

from sqlalchemy.orm import Session
from database import db_manager, SessionLocal
from users.user_model import User
from roles.role_model import Role
from security import get_password_hash

def setup_test_data():
    """
    Cria dados iniciais necessários para os testes.
    """
    db: Session = SessionLocal()
    
    try:
        print("🔧 Configurando dados para testes...")
        
        # 1. Garantir que existe a role 'admin'
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        if not admin_role:
            print("  📝 Criando role 'admin'...")
            admin_role = Role(name="admin")
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)
            print("  ✅ Role 'admin' criada!")
        else:
            print("  ℹ️  Role 'admin' já existe")
        
        # 2. Garantir que existe a role 'user'
        user_role = db.query(Role).filter(Role.name == "user").first()
        if not user_role:
            print("  📝 Criando role 'user'...")
            user_role = Role(name="user")
            db.add(user_role)
            db.commit()
            db.refresh(user_role)
            print("  ✅ Role 'user' criada!")
        else:
            print("  ℹ️  Role 'user' já existe")
        
        # 3. Criar usuário admin para testes
        test_admin_email = "admin@example.com"
        test_admin_password = "admin123"
        
        existing_admin = db.query(User).filter(User.email == test_admin_email).first()
        if not existing_admin:
            print(f"  👤 Criando usuário admin de teste: {test_admin_email}...")
            admin_user = User(
                email=test_admin_email,
                hashed_password=get_password_hash(test_admin_password),
                full_name="Test Admin User",
                role_id=admin_role.id
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print("  ✅ Usuário admin criado!")
            print(f"     Email: {test_admin_email}")
            print(f"     Senha: {test_admin_password}")
        else:
            print(f"  ℹ️  Usuário admin '{test_admin_email}' já existe")
        
        print("\n✨ Setup de testes concluído com sucesso!")
        print("\n📌 Credenciais para testes:")
        print(f"   Email: {test_admin_email}")
        print(f"   Senha: {test_admin_password}")
        print("\n💡 Certifique-se de que estas credenciais estão configuradas em tests/conftest.py")
        
    except Exception as e:
        print(f"\n❌ Erro durante o setup: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    # Garante que as tabelas existem
    print("🔨 Criando tabelas do banco de dados...")
    db_manager.create_all_tables()
    print("✅ Tabelas criadas/verificadas!")
    print()
    
    # Configura dados de teste
    setup_test_data()
