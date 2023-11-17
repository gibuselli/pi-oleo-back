from typing import Optional

from fastapi import Response, HTTPException
from sqlalchemy.orm import Session

from models.oil import OilRequest, Oil, OilDonationResponse
from models.oil_collect import OilCollectRequest, OilCollect
from models.user import User


def create_oil_donation(request: OilRequest, db: Session, user: User):
    new_oil = Oil(
        donator=user,
        oil_quantity=request.oil_quantity,
        cep=request.cep,
        district=request.district,
        address=request.address,
        address_number=request.address_number,
        complement=request.complement,
        day_available=request.day_available,
        telephone=request.telephone,
        is_available=True
    )
    try:
        db.add(new_oil)
    except:
        db.merge(new_oil)
    db.commit()

def create_oil_collect(request: OilCollectRequest, db: Session):
    oil_ids = request.ids
    collect_day = request.day

    for oil_id in oil_ids:
        oil = db.query(Oil).filter(Oil.id == oil_id).first()
        existing_collect = db.query(OilCollect).filter(OilCollect.oil == oil).first()

        if existing_collect:
            raise HTTPException(status_code=400, detail="Já existe uma retirada marcada para uma das doações selecionadas.")

        oil_collect = OilCollect(
            day=collect_day,
            oil=oil
        )

        db.add(oil_collect)
        oil.is_available = False
        db.commit()


def get_oil_donation(user: User, db: Session):
    oil: Optional[Oil] = db.query(Oil).filter(Oil.donator_id == user.id).first()

    if oil is None:
        return Response(status_code=404)

    if oil.is_available:
        return OilDonationResponse(oil_quantity=oil.oil_quantity, day=None)

    oil_collect: OilCollect = db.query(OilCollect).filter(OilCollect.oil == oil).first()

    return OilDonationResponse(oil_quantity=oil.oil_quantity, day=oil_collect.day.strftime("%Y-%m-%d"))





def get_available_donation_districts(db: Session):
    available_oil_list = db.query(Oil).filter(Oil.is_available).all()

    return sorted(set(oil.district for oil in available_oil_list))

def get_available_oil_by_district(district: str, db: Session):
    available_oil_list = db.query(Oil).filter(Oil.district == district, Oil.is_available).all()

    return [
            {
                "address": oil.address,
                "oil_quantity": oil.oil_quantity,
                "day_available": oil.day_available,
                "id": oil.id
             }
            for oil in available_oil_list
    ]
