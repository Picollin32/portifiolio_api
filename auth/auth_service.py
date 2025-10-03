# auth/auth_service.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pydantic import ValidationError
from jose import JWTError, jwt

from database import get_db
from users import user_repository
from roles import role_repository
from security import verify_password, get_password_hash, SECRET_KEY, ALGORITHM, TokenData
from users.user_model import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def authenticate_user(db: Session, email: str, password: str):
    user = user_repository.get_user_by_email(db, email=email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def register_user(db: Session, email: str, password: str, first_name: str, last_name: str, photo: str | None = None):
    """
    Registra um novo usuário com role 'user'
    Retorna o usuário criado ou levanta ValueError se o email já existe
    """
    # Verifica se o email já existe
    existing_user = user_repository.get_user_by_email(db, email=email)
    if existing_user:
        raise ValueError("Email já cadastrado")
    
    # Busca o role 'user'
    user_role = role_repository.get_role_by_name(db, name="user")
    if not user_role:
        raise ValueError("Role 'user' não encontrado. Execute init_db.py primeiro.")
    
    # Cria o usuário
    full_name = f"{first_name} {last_name}"
    hashed_password = get_password_hash(password)
    
    new_user = User(
        email=email,
        hashed_password=hashed_password,
        full_name=full_name,
        profile_image_url=photo,
        role_id=user_role.id
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        role: str = payload.get("role")
        if email is None or role is None:
            raise credentials_exception
        token_data = TokenData(email=email, role=role)
    except (JWTError, ValidationError):
        raise credentials_exception

    user = user_repository.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

def require_role(required_role_name: str):
    def role_checker(current_user: User = Depends(get_current_user)):
        if not current_user.role or current_user.role.name != required_role_name:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for this user role"
            )
        return current_user
    return role_checker