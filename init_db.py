"""
Script para inicializar o banco de dados com dados básicos
Cria um role admin e um usuário admin se não existirem
"""
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from users.user_model import User
from roles.role_model import Role
from security import get_password_hash

def init_db():
    """Inicializa o banco de dados com dados básicos"""
    
    # Cria as tabelas se não existirem
    Base.metadata.create_all(bind=engine)
    
    db: Session = SessionLocal()
    
    try:
        # Verifica se já existe o role admin
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        
        if not admin_role:
            print("Criando role 'admin'...")
            admin_role = Role(
                name="admin",
                description="Administrador do sistema"
            )
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)
            print(f"✅ Role 'admin' criado com ID: {admin_role.id}")
        else:
            print(f"✅ Role 'admin' já existe com ID: {admin_role.id}")
        
        # Verifica se já existe o usuário admin
        admin_user = db.query(User).filter(User.email == "admin@portfolio.com").first()
        
        if not admin_user:
            print("Criando usuário admin...")
            admin_user = User(
                email="admin@portfolio.com",
                hashed_password=get_password_hash("admin123"),
                full_name="Administrador",
                role_id=admin_role.id
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print(f"✅ Usuário admin criado com ID: {admin_user.id}")
            print("   Email: admin@portfolio.com")
            print("   Senha: admin123")
        else:
            print(f"✅ Usuário admin já existe com ID: {admin_user.id}")
        
        # Verifica se já existe o role user
        user_role = db.query(Role).filter(Role.name == "user").first()
        
        if not user_role:
            print("Criando role 'user'...")
            user_role = Role(
                name="user",
                description="Usuário comum do sistema"
            )
            db.add(user_role)
            db.commit()
            db.refresh(user_role)
            print(f"✅ Role 'user' criado com ID: {user_role.id}")
        else:
            print(f"✅ Role 'user' já existe com ID: {user_role.id}")
        
        print("\n🎉 Banco de dados inicializado com sucesso!")
        print("\n📝 Credenciais de acesso:")
        print("   Email: admin@portfolio.com")
        print("   Senha: admin123")
        
    except Exception as e:
        print(f"❌ Erro ao inicializar o banco de dados: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Inicializando banco de dados...")
    print("="*50)
    init_db()
    print("="*50)
