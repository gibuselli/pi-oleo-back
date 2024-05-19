from typing import Optional, List

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from models.user import User


class Collector(User):
    __tablename__ = "collector"

    id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    name = Column(String)
    document = Column(String)
    cep = Column(String)
    address = Column(String)
    district = Column(String)
    allow_delivery = Column(Boolean)

    __mapper_args__ = {
        'polymorphic_identity': 'collector'
    }


class CollectorRequest(BaseModel):
    name: str
    email: str
    password: str
    document: str
    telephone: Optional[str] = ''
    cep: str
    address: str
    district: str
    allow_delivery: bool


class CollectorResponse(BaseModel):
    name: str
    address: str


class CollectorListResponse(BaseModel):
    collectors: List[CollectorResponse]


def convert_to_collector_response(collector: Collector) -> CollectorResponse:
    return CollectorResponse(name=collector.name, address=collector.address)


def convert_list_to_response(collectors: List[Collector]) -> List[CollectorResponse]:
    return [convert_to_collector_response(collector) for collector in collectors]
