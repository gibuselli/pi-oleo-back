from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from models.oil_collect import OilCollectRequest
from models.user_type import UserType
from db.database import get_db
from models.oil import OilRequest, OilDonationResponse
from models.user import User
from services import oil_service, auth_service

router = APIRouter()


@router.post(path="/oil/", description="Cadastra uma quantidade de óleo a ser retirado")
def register_oil_donation(
        request: OilRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)):
    verify_user_type(UserType.DONATOR.value, current_user)

    oil_service.create_oil_donation(request, db, current_user)

    return Response(status_code=200)


@router.post(path="/oil/collect",
             description="Cadastra uma intenção de retirada de óleo para uma lista de doações",
             responses={
                 200: {"description": "Successful response"},
                 400: {
                         "description": "Bad request",
                         "content": {
                             "application/json": {
                                 "example":
                                 {
                                     "detail": "Já existe uma retirada marcada para uma das doações selecionadas."
                                 }
                             }
                         }
                     }
             })
def register_oil_collect(
        request: OilCollectRequest,
        db: Session = Depends(get_db),
        current_user: User = Depends(auth_service.get_current_user)):
    verify_user_type(UserType.COLLECTOR.value, current_user)

    oil_service.create_oil_collect(request, db)

    return Response(status_code=200)


@router.get(path="/oil/districts", description="Consulta bairros com doações em aberto")
def get_donation_districts(current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    verify_user_type(UserType.COLLECTOR.value, current_user)

    return oil_service.get_available_donation_districts(db)


@router.get(path="/oil/open/{district}", description="Consulta doações disponíveis de óleo por bairro")
def get_available_oil_by_district(
        district: str,
        current_user: User = Depends(auth_service.get_current_user),
        db: Session = Depends(get_db)):
    verify_user_type(UserType.COLLECTOR.value, current_user)

    return oil_service.get_available_oil_by_district(district, db)


@router.get(path="/my-oil/",
            description="Consulta a doação do usuário e data de retirada",
            response_model=OilDonationResponse)
def get_oil_donation(current_user: User = Depends(auth_service.get_current_user), db: Session = Depends(get_db)):
    verify_user_type(UserType.DONATOR.value, current_user)

    return oil_service.get_oil_donation(current_user, db)


def verify_user_type(user_type: str, current_user: User):
    if current_user.user_type != user_type:
        raise HTTPException(status_code=400, detail="Tipo de usuário incorreto.")
