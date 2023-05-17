from fastapi import APIRouter, status, HTTPException, Response, Depends
from db.db_inc import engine, Base
from modeles.role import Role
from sqlalchemy.orm import sessionmaker
from routers.login import get_current_user
from utils.admin import is_admin, is_maintainer
router = APIRouter()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@router.get("/roles")
def read_roles(current_user: Role = Depends(get_current_user)):
    if not is_maintainer(current_user):
        raise HTTPException(status_code=401, detail="Not authorized to read roles")
    db = SessionLocal()
    roles = db.query(Role).all()
    return roles

