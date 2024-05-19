from sqlalchemy.orm import Session

from models.collector import Collector, CollectorRequest, CollectorResponse, convert_list_to_response
from models.donator import Donator, DonatorRequest
from models.user import User
from services.auth_service import hash_password


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_donator_by_user_id(db: Session, user_id: int) -> Donator:
    return db.query(Donator).filter(Donator.id == user_id).first()


def get_delivery_collectors(db: Session):
    collectors = db.query(Collector).filter(Collector.allow_delivery).all()
    return convert_list_to_response(collectors)

def update_user_score(donator: Donator, donated_oil: int):
    donator.score += donated_oil
    
    donator_level = donator.score // 10
    
    donator.level = donator_level
    


def create_donator(db: Session, request: DonatorRequest):
    hashed_password = hash_password(request.password)

    new_donator = Donator(
        name=request.name,
        surname=request.surname,
        email=request.email,
        hashed_password=hashed_password,
        telephone=request.telephone,
        score=0,
        level=0
    )

    db.add(new_donator)
    db.commit()


def create_collector(db: Session, request: CollectorRequest):
    hashed_password = hash_password(request.password)

    new_collector = Collector(
        name="nome",
        document=request.document,
        email=request.email,
        telephone=request.telephone,
        hashed_password=hashed_password,
        cep=request.cep,
        address=request.address,
        district=request.district,
        allow_delivery=request.allow_delivery
    )

    db.add(new_collector)
    db.commit()
