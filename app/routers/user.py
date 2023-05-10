from sqlalchemy.orm import sessionmaker, Session
from fastapi import APIRouter, status, HTTPException, Response, Depends
from db.db_inc import engine, Base
from modeles.user import User, UserCreate
from modeles.role import Role
from modeles.company import Company
from routers.login import get_current_user
import bcrypt

router = APIRouter()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@router.get("/users")
def read_users():
    db = SessionLocal()
    users = db.query(User).all()
    return users


# @router.get("/users/{user_id}")
# def read_user(user_id: int):
#     db = SessionLocal()
#     user = db.query(User).filter(User.id == user_id).first()
#     return user


@router.post("/users")
def create_user(
        user: UserCreate,
        current_user: User = Depends(get_current_user)
):
    """
    Role 1: User;
    Role 2: Admin;
    Role 3: Maintainer;
    """
    db = SessionLocal()
    if current_user.role_id != 2 and current_user.role_id != 3:
        raise HTTPException(
            status_code=401,
            detail="Not authorized to create users"
        )
    else:
        if user.role_id == 0:
            user.role_id = 1
        if not role_exists(db, user.role_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid role_id"
            )
        if user.role_id > current_user.role_id:
            raise HTTPException(
                status_code=401,
                detail="Cannot create user with a role greater than your own"
            )

        # Hash the password
        hashed_password = bcrypt.hashpw(
            user.password.encode('utf-8'),
            bcrypt.gensalt()
        )

        if current_user.role_id == 3:
            if user.company_id is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Missing company_id"
                )
            else:
                company = db.query(Company).filter_by(
                    id=user.company_id
                ).first()
                if company is None:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid company_id"
                    )
        else:
            user.company_id = current_user.company_id

        new_user = User(
            username=user.username,
            email=user.email,
            password=hashed_password,
            role_id=user.role_id,
            company_id=user.company_id,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


def role_exists(db: Session, role_id: int) -> bool:
    return db.query(Role).filter(Role.id == role_id).first() is not None
