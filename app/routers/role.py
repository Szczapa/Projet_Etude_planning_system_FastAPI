from fastapi import APIRouter, status, HTTPException, Response, Depends
from db.db_inc import engine, Base
from modeles.role import Role
from sqlalchemy.orm import sessionmaker
from routers.login import get_current_user

router = APIRouter()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@router.get("/roles")
def read_roles(current_user: Role = Depends(get_current_user)):
    if current_user.role_id != 3:
        raise HTTPException(status_code=401, detail="Not authorized to read roles")
    db = SessionLocal()
    roles = db.query(Role).all()
    return roles


# @router.get("/roles/{role_id}")
# def read_role(role_id: int):
#     db = SessionLocal()
#     role = db.query(Role).filter(Role.id == role_id).first()
#     return role
