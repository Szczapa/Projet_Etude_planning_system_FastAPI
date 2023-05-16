from sqlalchemy.orm import sessionmaker, Session
from fastapi import APIRouter, status, HTTPException, Response, Depends
from db.db_inc import engine, Base
from modeles.user import User, UserCreate, UserUpdate
from modeles.role import Role
from modeles.company import Company
from routers.login import get_current_user
from sqlalchemy import func
import bcrypt
from cryptography.fernet import Fernet
import base64

key = b'OP7RRCuQzEpyIGaoiywUqh_S068cJbtXCNGPF47vzQs='

fernet = Fernet(key)

router = APIRouter()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@router.get("/users")
def read_users(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    if current_user.role_id == 3:
        users = db.query(User).all()
    elif current_user.role_id == 2:
        users = db.query(User).filter(User.company_id == current_user.company_id).all()

    decrypted_users = []
    for user in users:
        decrypted_username = fernet.decrypt(base64.urlsafe_b64decode(user.username.encode('utf-8'))).decode('utf-8')
        decrypted_email = fernet.decrypt(base64.urlsafe_b64decode(user.email.encode('utf-8'))).decode('utf-8')

        decrypted_user = {
            'username': decrypted_username,
            'email': decrypted_email,
            'password': user.password,
            'role_id': user.role_id,
            'company_id': user.company_id
        }
        decrypted_users.append(decrypted_user)

    return decrypted_users


# @router.get("/users/{user_id}")
# def read_user(user_id: int):
#     db = SessionLocal()
#     user = db.query(User).filter(User.id == user_id).first()
#     return user


@router.post("/user")
def create_user(
        user: UserCreate
        , current_user: User = Depends(get_current_user)
):
    """
    Role 1: User;
    Role 2: Admin;
    Role 3: Maintainer;
    """
    db = SessionLocal()
    if current_user.role_id != 3:
        raise HTTPException(
            status_code=401,
            detail="Not authorized to create users"
        )
    else:
        if user.role_id == 0:
            user.role_id = 1
        if not role_exists(db, user.role_id):
            raise HTTPException(
                status_code=400,
                detail="Invalid role_id"
            )

    # Hash the password
    hashed_password = bcrypt.hashpw(
        user.password.encode('utf-8'),
        bcrypt.gensalt()
    )

    if user.company_id is None:
        raise HTTPException(
            status_code=400,
            detail="Missing company_id"
        )
    else:
        company = db.query(Company).filter_by(
            id=user.company_id
        ).first()
        if company is None:
            raise HTTPException(
                status_code=400,
                detail="Invalid company_id"
            )

    if email_exists(db, user.email.lower()):
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    encrypted_username = fernet.encrypt(user.username.encode('utf-8'))
    encrypted_email = fernet.encrypt(user.email.lower().encode('utf-8'))

    new_user = User(
        username=base64.urlsafe_b64encode(encrypted_username).decode('utf-8'),
        email=base64.urlsafe_b64encode(encrypted_email).decode('utf-8'),
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


def email_exists(db: Session, email: str) -> bool:
    users = db.query(User).all()

    if not users:
        return False

    for user in users:
        decrypted_email = fernet.decrypt(base64.urlsafe_b64decode(user.email.encode('utf-8'))).decode('utf-8')
        if decrypted_email.lower() == email.lower():
            return True

    return False


@router.delete("/user/{user_id}")
def delete_user(
        user_id: int,
        current_user: User = Depends(get_current_user)
):
    db = SessionLocal()
    if current_user.role_id == 3:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        else:
            db.delete(user)
            db.commit()
            return Response(status_code=204)
    elif current_user.role_id == 2:
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        elif user.company_id != current_user.company_id:
            raise HTTPException(
                status_code=401,
                detail="Not authorized to delete this user"
            )
        else:
            db.delete(user)
            db.commit()
            return Response(status_code=204)


@router.put("/user/{user_id}")
def update_user(user_id: int, user: UserUpdate, current_user: User = Depends(get_current_user)):
    db = SessionLocal()

    # Récupérer l'utilisateur cible dans la base de données
    user_to_update = db.query(User).filter(User.id == user_id).first()

    # Vérifier si l'utilisateur existe
    if user_to_update is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Vérifier les autorisations de mise à jour en fonction du rôle de l'utilisateur actuel
    if current_user.role_id == 3:
        # Rang 3 : Autorisé à modifier tous les attributs
        if user.username is not None:
            user_to_update.username = user.username
        if user.email is not None:
            user_to_update.email = user.email
        if user.role_id is not None:
            user_to_update.role_id = user.role_id
        if user.password is not None:
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
            user_to_update.password = hashed_password

    elif current_user.role_id == 2:
        # Rang 2 : Autorisé à modifier username, email et rôle (inférieur ou égal à 2) mais pas le mot de passe
        if user.username is not None:
            user_to_update.username = user.username
        if user.email is not None:
            user_to_update.email = user.email
        if user.role_id is not None and user.role_id <= 2:
            user_to_update.role_id = user.role_id
        if user.password is not None:
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
            user_to_update.password = hashed_password

    elif current_user.id == user_id:
        # Utilisateur lui-même : Autorisé à modifier username, email et mot de passe
        if user.username is not None:
            user_to_update.username = user.username
        if user.email is not None:
            user_to_update.email = user.email
        if user.password is not None:
            hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
            user_to_update.password = hashed_password

    else:
        # Pas autorisé à mettre à jour l'utilisateur
        raise HTTPException(status_code=401, detail="Not authorized to update this user")

    db.commit()
    db.refresh(user_to_update)
    return user_to_update
