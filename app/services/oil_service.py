from sqlalchemy.orm import Session

from models.oil import OilRequest, Oil
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
