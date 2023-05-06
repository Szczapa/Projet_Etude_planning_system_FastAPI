from sqlalchemy.orm import sessionmaker, Session
from fastapi import APIRouter, status, HTTPException, Response
from db.db_inc import engine, Base
from modeles.user import User, UserCreate
from modeles.role import Role
import bcrypt

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


@router.post("/users")
def create_user(user: UserCreate):
    """
    Role 1: User;
    Role 2: Admin;
    Role 3: Maintainer;
    """
    db = SessionLocal()
    if not role_exists(db, user.role_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role_id")

    # Hash the password
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        role_id=user.role_id,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def role_exists(db: Session, role_id: int) -> bool:
    return db.query(Role).filter(Role.id == role_id).first() is not None


def crypt_password(password: str) -> str:
    return password