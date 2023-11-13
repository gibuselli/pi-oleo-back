from datetime import date
from typing import List

from pydantic import BaseModel
from sqlalchemy import Column, Integer, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship

from models.base import Base


class OilCollect(Base):
    __tablename__ = "oil_collect"

    id = Column(Integer, primary_key=True)
    oil_id = Column(Integer, ForeignKey('oil.id'), nullable=False)
    day = Column(Date, nullable=False)
    is_collected = Column(Boolean, nullable=False, default=False)

    # relationships
    oil = relationship("Oil", back_populates="oil_collect")


class OilCollectRequest(BaseModel):
    day: date
    ids: List[int]

