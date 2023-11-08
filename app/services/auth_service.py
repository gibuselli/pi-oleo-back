from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config import SECRET_KEY, ALGORITHM
from db.database import get_db
from models.user import User

# Password hashing settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authenticate")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: Optional[str] = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401,
                                detail="Erro ao validar credenciais",
                                headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        raise HTTPException(status_code=401,
                            detail="Erro ao validar credenciais",
                            headers={"WWW-Authenticate": "Bearer"})

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Erro ao validar credenciais")

    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.email == username).first()

    db.close()

    if not user:
        return False

    if not pwd_context.verify(password, user.hashed_password):
        return False

    return user

def hash_password(password: str):
    return pwd_context.hash(password)

def validate_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401,
                                detail="Erro ao validar token",
                                headers={"WWW-Authenticate": "Bearer"})

        expiration_time = payload.get("exp")
        current_time = datetime.utcnow()

        if expiration_time is not None and expiration_time < current_time.timestamp():
            raise HTTPException(status_code=401,
                                detail="Token expirado",
                                headers={"WWW-Authenticate": "Bearer"})

    except JWTError:
        raise HTTPException(status_code=401,
                            detail="Erro ao validar token",
                            headers={"WWW-Authenticate": "Bearer"})

    return {"email": email}
