from typing import Optional

from sqlalchemy import Column, Integer, String, ForeignKey
from pydantic import BaseModel

from models.user import User


class Donator(User):
    __tablename__ = "donator"

    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    telephone = Column(String, nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'donator'
    }

class DonatorRequest(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    telephone: Optional[str] = ''
    user_type: str = 'doador'


class DonatorResponse(BaseModel):
    msg: str


class DonatorListResponse(BaseModel):
    email: str
    name: str
    surname: str
    telephone: str
