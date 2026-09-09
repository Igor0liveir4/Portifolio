import sys
import getpass
import os

# Garante que o Python encontre o módulo 'app' independente de onde o script for executado
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import SessionLocal, engine, Base
from app.models.user import User
from app.core import security

def create_initial_admin():
    """
    Script interativo via linha de comando para registrar
    o primeiro usuário administrador com senha criptografada.
    """
    print("==========================================")
    print("   Criação de Usuário Administrador (Portfolio)   ")
    print("==========================================\n")

    # Garante que as tabelas existam no banco antes de tentar inserir
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        full_name = input("Nome completo: ").strip()
        email = input("E-mail de acesso: ").strip().lower()

        if not full_name or not email:
            print("\n❌ Erro: Nome e e-mail são obrigatórios.")
            return

        # 2. Verifica se o e-mail já existe
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            print(f"\n⚠️  Atenção: Já existe um usuário cadastrado com o e-mail '{email}'.")
            return

        # 3. Leitura oculta e validação da senha
        password = getpass.getpass("Digite a senha: ")
        password_confirm = getpass.getpass("Confirme a senha: ")

        if password != password_confirm:
            print("\n❌ Erro: As senhas digitadas não coincidem.")
            return

        if len(password) < 6:
            print("\n❌ Erro: A senha deve ter pelo menos 6 caracteres.")
            return

        # 4. Criação do hash da senha e salvamento no banco
        hashed_pwd = security.get_password_hash(password)

        admin_user = User(
            full_name=full_name,
            email=email,
            hashed_password=hashed_pwd,
            is_active=True
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print("\n✅ Usuário administrador criado com sucesso!")
        print(f"   ID: {admin_user.id}")
        print(f"   Nome: {admin_user.full_name}")
        print(f"   E-mail: {admin_user.email}")

    except Exception as e:
        db.rollback()
        print(f"\n❌ Ocorreu um erro ao criar o usuário: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_initial_admin()