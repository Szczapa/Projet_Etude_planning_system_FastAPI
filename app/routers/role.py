from fastapi import APIRouter, status, HTTPException, Response
from db.db_inc import engine, Base
from modeles.role import Role
from sqlalchemy.orm import sessionmaker

router = APIRouter()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@router.get("/roles")
def read_roles():
    db = SessionLocal()
    roles = db.query(Role).all()
    return roles


@router.get("/roles/{role_id}")
def read_role(role_id: int):
    db = SessionLocal()
    role = db.query(Role).filter(Role.id == role_id).first()
    return role
