from sqlalchemy.orm import sessionmaker, Session
from fastapi import APIRouter, status, HTTPException, Depends, Response
from db.db_inc import engine, Base
from modeles.user import User, UserOut
import bcrypt
from jwt import InvalidTokenError as PyJWTError
from jwt import decode, encode
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from cryptography.fernet import Fernet
import base64

key = b'OP7RRCuQzEpyIGaoiywUqh_S068cJbtXCNGPF47vzQs='

# Initialisation de la clé Fernet
fernet = Fernet(key)

router = APIRouter()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = "Mykey"
ALGORITHM = "HS256"


def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


def create_access_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        decoded_token = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded_token
    except PyJWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    decoded_token = decode_access_token(token)
    if not decoded_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    db = SessionLocal()
    user = db.query(User).filter(User.id == decoded_token.get('id')).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.post("/login", response_model=dict)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
        Username = email;
    """

    db = SessionLocal()
    users = db.query(User).all()
    for user in users:
        decrypted_email = fernet.decrypt(base64.urlsafe_b64decode(user.email.encode('utf-8'))).decode('utf-8')
        if decrypted_email.lower() == form_data.username.lower():
            break
    else:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": user.email, "id": user.id, "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def get_current_logged_in_user(current_user: User = Depends(get_current_user)):
    return UserOut(id=current_user.id,
                   email=current_user.email,
                   role_id=current_user.role_id,
                   company_id=current_user.company_id,
                   username=current_user.username)
