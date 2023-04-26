from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, status, HTTPException, Response
from db.db_inc import engine, Base
from modeles.user import User

router = APIRouter()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@router.get("/users")
def read_users():
    db = SessionLocal()
    users = db.query(User).all()
    return users


@router.get("/users/{user_id}")
def read_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    return user
