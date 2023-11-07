from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from models.user import User


class Collector(User):
    __tablename__ = "collector"

    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    document = Column(String)
    telephone = Column(String)
    cep = Column(String)
    address = Column(String)
    district = Column(String)
    allow_delivery = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'collector'
    }


class CollectorRequest(BaseModel):
    email: str
    password: str
    document: str
    telephone: Optional[str] = ''
    cep: str
    address: str
    district: str
    allow_delivery: bool
    user_type: str = 'retirador'

class CollectorResponse(BaseModel):
    msg: str


class CollectorListResponse(BaseModel):
    email: str
    telephone: str
    cep: str
    address: str
    district: str
    document: str
    allow_delivery: bool
