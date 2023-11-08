from fastapi import Response
from sqlalchemy.orm import Session

from models.oil import OilRequest, Oil, OilDonationResponse
from models.user import User


def create_oil_donation(request: OilRequest, db: Session, user: User):
    new_oil = Oil(
        user=user.id,
        oil_quantity=request.oil_quantity,
        cep=request.cep,
        district=request.district,
        address=request.address,
        address_number=request.address_number,
        complement=request.complement,
        day_available=request.day_available,
        telephone=request.telephone
    )

    db.add(new_oil)
    db.commit()

def get_oil_donation(user: User, db: Session):
    user_oil: Oil = db.query(Oil).join(User).filter(User.id == user.id).one_or_none()

    if user_oil is not None:
        return OilDonationResponse(oil_quantity=user_oil.oil_quantity, day=user_oil.day_available)

    return Response(status_code=400)
