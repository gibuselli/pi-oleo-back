from typing import Optional

from sqlalchemy import Column, Integer, String, ForeignKey
from pydantic import BaseModel
from sqlalchemy.orm import relationship

from models.user import User


class Donator(User):
    __tablename__ = "donator"

    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    telephone = Column(String, nullable=True)

    oil = relationship("Oil", back_populates="donator", uselist=False)

    __mapper_args__ = {
        'polymorphic_identity': 'donator'
    }

class DonatorRequest(BaseModel):
    name: str
    surname: str
    email: str
    password: str
    telephone: Optional[str] = ''


class DonatorListResponse(BaseModel):
    email: str
    name: str
    surname: str
    telephone: str
