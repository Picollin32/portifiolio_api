# roles/role_service.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from . import role_repository, role_model

def create_new_role(db: Session, role: role_model.RoleCreate):
    db_role = role_repository.get_role_by_name(db, name=role.name)
    if db_role:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role name already exists")
    return role_repository.create_role(db=db, role=role)

def get_all(db: Session):
    return role_repository.get_all_roles(db)

def get_role_by_id(db: Session, role_id: int):
    db_role = role_repository.get_role_by_id(db, role_id)
    if not db_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return db_role

def update_role(db: Session, role_id: int, role: role_model.RoleCreate):
    # Verifica se a role existe
    db_role = role_repository.get_role_by_id(db, role_id)
    if not db_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    
    # Verifica se o novo nome já existe em outra role
    existing_role = role_repository.get_role_by_name(db, name=role.name)
    if existing_role and existing_role.id != role_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Role name already exists")
    
    return role_repository.update_role(db=db, role_id=role_id, role=role)

def delete_role(db: Session, role_id: int):
    db_role = role_repository.get_role_by_id(db, role_id)
    if not db_role:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return role_repository.delete_role(db=db, role_id=role_id)