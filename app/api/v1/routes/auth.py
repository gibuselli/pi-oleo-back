import random
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config import ACCESS_TOKEN_EXPIRE_MINUTES
from models.user import User
from services import auth_service
from db.database import get_db

router = APIRouter()


@router.post(path="/authenticate/")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=401, detail="Usuário ou senha incorretos!")

    access_token = auth_service.create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/quem-vai-pagar-o-habibao/")
def protected_resource(current_user: User = Depends(auth_service.get_current_user)):
    esfiha_payer = ["Ivan",
                    "Mari",
                    "Bob",
                    "Rodrigo",
                    "Edson",
                    "Ocimar",
                    "Nayara"
                    ]

    return {
        "msg": "Parabéns! Você acessou o endpoint secreto e agora vai descobrir quem vai pagar o próximo rodízio do "
               "Habibão!",
        "rodizio_por_conta_de": random.choice(esfiha_payer),
        "user": current_user.email}


@router.get("/current-user/")
def get_current_user(current_user: User = Depends(auth_service.get_current_user)):
    return {"email": current_user.email, "user_type": current_user.user_type}

@router.post("/validate_token/")
def validate_token(token: str):
    return auth_service.validate_token(token)
