"""
Script de demonstração dos padrões de design implementados.

Este script mostra como os padrões funcionam na prática.
Execute apenas após configurar o banco de dados.
"""

from database import db_manager, get_db
from users.user_factory import UserFactory, UserValidator
from users.user_repository import UserRepository
from users.user_service import UserService
from users.user_model import UserCreate, UserUpdate


def demonstrar_singleton():
    """Demonstra o Singleton Pattern do DatabaseManager."""
    print("\n" + "="*60)
    print("1. SINGLETON PATTERN - DatabaseManager")
    print("="*60)
    
    # Cria duas "instâncias" - mas são o mesmo objeto
    manager1 = db_manager
    from database import DatabaseManager
    manager2 = DatabaseManager()
    
    print(f"manager1 id: {id(manager1)}")
    print(f"manager2 id: {id(manager2)}")
    print(f"São o mesmo objeto? {manager1 is manager2}")
    print(f"✅ Singleton garante uma única instância!")
    
    # Mostra propriedades
    print(f"\nEngine: {manager1.engine}")
    print(f"Session Factory: {manager1.session_local}")


def demonstrar_factory():
    """Demonstra o Factory Pattern para criação de Users."""
    print("\n" + "="*60)
    print("2. FACTORY PATTERN - UserFactory")
    print("="*60)
    
    # Criação consistente de User com validações
    print("\n📝 Criando User com Factory...")
    
    try:
        # Tentativa com dados válidos
        user_entity = UserFactory.create_user_entity(
            email="teste@example.com",
            password="senha123456",
            role_id=1,
            full_name="João Silva"
        )
        print(f"✅ User criado com sucesso!")
        print(f"   Email normalizado: {user_entity.email}")
        print(f"   Senha hasheada: {user_entity.hashed_password[:20]}...")
        print(f"   Nome: {user_entity.full_name}")
        
    except ValueError as e:
        print(f"❌ Erro: {e}")
    
    # Tentativa com senha inválida
    print("\n🔍 Testando validação de senha curta...")
    try:
        invalid_user = UserFactory.create_user_entity(
            email="invalido@example.com",
            password="123",  # Muito curta!
            role_id=1
        )
    except ValueError as e:
        print(f"✅ Validação funcionou: {e}")


def demonstrar_repository():
    """Demonstra o Repository Pattern."""
    print("\n" + "="*60)
    print("3. REPOSITORY PATTERN - UserRepository")
    print("="*60)
    
    print("\n📚 Repository abstrai operações CRUD:")
    print("   • get_by_id(user_id)")
    print("   • get_by_email(email)")
    print("   • get_all(skip, limit)")
    print("   • create(user, role_id)")
    print("   • update(user, data)")
    print("   • delete(user)")
    
    print("\n✅ Benefícios:")
    print("   • Queries centralizadas")
    print("   • Fácil de mockar em testes")
    print("   • Lógica de persistência isolada")


def demonstrar_service():
    """Demonstra a Service Layer."""
    print("\n" + "="*60)
    print("4. SERVICE LAYER - UserService")
    print("="*60)
    
    print("\n🧠 Service Layer gerencia lógica de negócio:")
    print("   • Validação de email único")
    print("   • Validação de role existente")
    print("   • Tratamento de exceções")
    print("   • Orquestração entre repositórios")
    
    print("\n✅ Benefícios:")
    print("   • Regras de negócio centralizadas")
    print("   • Controllers mais limpos")
    print("   • Reutilização de lógica")


def demonstrar_arquitetura_camadas():
    """Demonstra a Arquitetura em Camadas."""
    print("\n" + "="*60)
    print("5. LAYERED ARCHITECTURE - Fluxo de Dados")
    print("="*60)
    
    print("\n📊 Fluxo de criação de usuário:")
    print()
    print("   1. CONTROLLER (user_controller.py)")
    print("      ↓ Recebe POST /users")
    print("      ↓ Valida UserCreate schema (Pydantic)")
    print()
    print("   2. SERVICE (user_service.py)")
    print("      ↓ Valida email único")
    print("      ↓ Valida role existe")
    print("      ↓ Aplica regras de negócio")
    print()
    print("   3. REPOSITORY (user_repository.py)")
    print("      ↓ Usa Factory para criar entidade")
    print("      ↓ Executa INSERT no banco")
    print()
    print("   4. FACTORY (user_factory.py)")
    print("      ↓ Valida dados")
    print("      ↓ Hasheia senha")
    print("      ↓ Normaliza email")
    print("      ↓ Cria objeto User")
    print()
    print("   5. DATABASE (database.py)")
    print("      ↓ DatabaseManager (Singleton)")
    print("      ↓ Session do banco")
    print("      ↓ PostgreSQL")
    print()
    print("   ✅ Usuário criado com sucesso!")


def demonstrar_principios_solid():
    """Demonstra os princípios SOLID aplicados."""
    print("\n" + "="*60)
    print("6. PRINCÍPIOS SOLID APLICADOS")
    print("="*60)
    
    print("\n🎯 S - Single Responsibility Principle")
    print("   • Controller: apenas HTTP")
    print("   • Service: apenas lógica de negócio")
    print("   • Repository: apenas persistência")
    print("   • Factory: apenas criação de objetos")
    
    print("\n🎯 O - Open/Closed Principle")
    print("   • Fácil adicionar novos endpoints sem modificar existentes")
    print("   • Fácil adicionar novos services")
    
    print("\n🎯 L - Liskov Substitution Principle")
    print("   • Repositories podem ser substituídos (ex: mock em testes)")
    
    print("\n🎯 I - Interface Segregation Principle")
    print("   • Cada camada tem interface específica")
    
    print("\n🎯 D - Dependency Inversion Principle")
    print("   • Camadas dependem de abstrações (Session, Schemas)")


def demonstrar_beneficios():
    """Demonstra os benefícios da arquitetura."""
    print("\n" + "="*60)
    print("7. BENEFÍCIOS DA ARQUITETURA")
    print("="*60)
    
    print("\n✅ TESTABILIDADE")
    print("   • Cada camada testável isoladamente")
    print("   • Fácil criar mocks")
    print("   • Testes unitários simples")
    
    print("\n✅ MANUTENIBILIDADE")
    print("   • Código organizado e limpo")
    print("   • Fácil encontrar onde fazer mudanças")
    print("   • Onboarding de devs mais rápido")
    
    print("\n✅ ESCALABILIDADE")
    print("   • Fácil adicionar novos recursos")
    print("   • Pool de conexões otimizado")
    print("   • Arquitetura preparada para crescimento")
    
    print("\n✅ REUTILIZAÇÃO")
    print("   • Repositories usados por múltiplos services")
    print("   • Factory centraliza criação")
    print("   • Validators reutilizáveis")


def main():
    """Executa todas as demonstrações."""
    print("\n" + "█"*60)
    print("█  DEMONSTRAÇÃO DE PADRÕES DE DESIGN")
    print("█  Portfólio API - Backend FastAPI")
    print("█"*60)
    
    demonstrar_singleton()
    demonstrar_factory()
    demonstrar_repository()
    demonstrar_service()
    demonstrar_arquitetura_camadas()
    demonstrar_principios_solid()
    demonstrar_beneficios()
    
    print("\n" + "="*60)
    print("✨ DEMONSTRAÇÃO CONCLUÍDA!")
    print("="*60)
    print("\n📚 Para mais informações, consulte:")
    print("   • DESIGN_PATTERNS.md")
    print("   • ARCHITECTURE.md")
    print("   • IMPLEMENTATION_GUIDE.md")
    print()


if __name__ == "__main__":
    main()
