from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from db.database import get_db
from models.collector import CollectorRequest, CollectorListResponse
from models.donator import DonatorRequest, DonatorListResponse
from services import user_service

router = APIRouter()


@router.get(path="/donators/", description="Lista todos os usuários doadores", response_model=List[DonatorListResponse])
def get_all_donators(db: Session = Depends(get_db)):
    return user_service.get_donators(db)

@router.get(path="/collectors/",
            description="Lista todos os usuários coletores",
            response_model=List[CollectorListResponse])
def get_all_collectors(db: Session = Depends(get_db)):
    return user_service.get_collectors(db)


@router.post(path="/donator/", description="Cria um usuário doador")
def create_donator(request: DonatorRequest, db: Session = Depends(get_db)):
    if request.user_type != "doador":
        raise HTTPException(status_code=400, detail="Tipo de usuário incorreto.")

    existing_donator = user_service.get_user_by_email(db, request.email)

    if existing_donator:
        raise HTTPException(status_code=409, detail="O usuário informado já é cadastrado.")

    user_service.create_donator(db, request)

    return Response(status_code=200)


@router.post(path="/collector/", description="Cria um usuário retirador")
def create_collector(request: CollectorRequest, db: Session = Depends(get_db)):
    if request.user_type != "retirador":
        raise HTTPException(status_code=400, detail="Tipo de usuário incorreto.")

    existing_collector = user_service.get_user_by_email(db, request.email)

    if existing_collector:
        raise HTTPException(status_code=409, detail="O usuário informado já é cadastrado.")

    user_service.create_collector(db, request)

    return Response(status_code=200)
