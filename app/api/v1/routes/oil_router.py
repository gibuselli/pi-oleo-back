from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from db.database import get_db
from models.oil import OilRequest
from models.user import User
from services import oil_service, auth_service

router = APIRouter()

@router.post(path="/oil/", description="Cadastra uma quantidade de óleo a ser retirado")
def register_oil_donation(
        request: OilRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)):
    if current_user.user_type != "donator":
        print(current_user.user_type)
        raise HTTPException(status_code=400, detail="Tipo de usuário incorreto.")

    oil_service.create_oil_donation(request, db, current_user)

    return Response(status_code=201)

@router.get(path="/my-oil/", description="Consulta quando a doação será retirada")
def get_oil_donation(current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    return oil_service.get_oil_donation(current_user, db)
