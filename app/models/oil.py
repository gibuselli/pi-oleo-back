from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from models.base import Base


class Oil(Base):
    __tablename__ = "oil"

    id = Column(Integer, primary_key=True)
    donator_id = Column(Integer, ForeignKey('donator.id'), nullable=False)
    oil_quantity = Column(Integer, nullable=False)
    cep = Column(String, nullable=False)
    district = Column(String, nullable=False)
    address = Column(String, nullable=False)
    address_number = Column(String, nullable=False)
    complement = Column(String, nullable=True)
    day_available = Column(String, nullable=True)
    telephone = Column(String, nullable=True)
    is_available = Column(Boolean, nullable=False)

    # relationships
    donator = relationship("Donator", back_populates="oil", uselist=False)
    oil_collect = relationship("OilCollect", back_populates="oil", uselist=False)

class OilRequest(BaseModel):
    oil_quantity: int
    cep: str
    district: str
    address: str
    address_number: str
    complement: Optional[str] = ''
    day_available: Optional[str] = ''
    telephone: Optional[str] = ''

class OilDonationResponse(BaseModel):
    oil_quantity: int
    day: Optional[str] = ''
