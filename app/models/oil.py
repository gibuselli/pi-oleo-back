from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey

from models.base import Base


class Oil(Base):
    __tablename__ = "oil"

    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('user.id'), nullable=False)
    oil_quantity = Column(Integer, nullable=False)
    cep = Column(String, nullable=False)
    district = Column(String, nullable=False)
    address = Column(String, nullable=False)
    address_number = Column(Integer, nullable=False)
    complement = Column(String, nullable=True)
    day_available = Column(String, nullable=True)
    telephone = Column(String, nullable=True)

class OilRequest(BaseModel):
    oil_quantity: int
    cep: str
    district: str
    address: str
    address_number: int
    complement: Optional[str] = ''
    day_available: Optional[str] = ''
    telephone: Optional[str] = ''
