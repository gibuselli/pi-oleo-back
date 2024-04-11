import os

import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models.base import Base
from models.collector import Collector
from models.donator import Donator
from models.oil import Oil
from models.oil_collect import OilCollect

DB_URL = os.getenv("DB_URL")

engine = create_engine(DB_URL, connect_args={'check_same_thread': False})
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = Base.metadata


def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    db = sessionlocal()
    with engine.connect() as connection:
        try:
            Base.metadata.create_all(bind=engine)
            seed_data()
        except Exception as e:
            print(f"Error creating tables: {str(e)}")
        finally:
            db.close()


def drop_tables():
    with engine.connect() as connection:
        try:
            Base.metadata.drop_all(bind=engine)
        except Exception as e:
            print(f"Error dropping tables: {str(e)}")


def seed_data():
    db = sessionlocal()

    try:
        doador1 = Donator(
            email="doador1@doador.com",
            name="Aline Silva",
            surname="fernandes",
            hashed_password="$2b$12$2UGp20WpjEaU7VJiBw4oYO.Um9JlcX6E7PphX1fnLqe8g2MKjxJvO",
            telephone="11912345678"
        )

        doador2 = Donator(
            email="doador2@doador.com",
            name="Nicolas Fernandes",
            surname="da silva",
            hashed_password="$2b$12$2UGp20WpjEaU7VJiBw4oYO.Um9JlcX6E7PphX1fnLqe8g2MKjxJvO",
            telephone="11912345678"
        )

        doador3 = Donator(
            email="doador3@doador.com",
            name="Pedro Silva Albuquerque",
            surname="de fernandes",
            hashed_password="$2b$12$2UGp20WpjEaU7VJiBw4oYO.Um9JlcX6E7PphX1fnLqe8g2MKjxJvO",
            telephone="11912345678"
        )

        doador4 = Donator(
            email="doador4@doador.com",
            name="Giovani Nascimento",
            surname="quatro",
            hashed_password="$2b$12$2UGp20WpjEaU7VJiBw4oYO.Um9JlcX6E7PphX1fnLqe8g2MKjxJvO",
            telephone="11912345678"
        )

        retirador1 = Collector(
            name="Eco ABC",
            document="12345560-12",
            email="retirador@retirador.com",
            telephone="11912345678",
            hashed_password="$2b$12$2UGp20WpjEaU7VJiBw4oYO.Um9JlcX6E7PphX1fnLqe8g2MKjxJvO",
            cep="0123012",
            address="Av. Pery Ronchetti, 1625",
            district="Nova Petrópolis",
            allow_delivery=True
        )

        retirador2 = Collector(
            name="Pego Oleo",
            document="12345560-12",
            email="retirador1@retirador.com",
            telephone="11912345678",
            hashed_password="$2b$12$2UGp20WpjEaU7VJiBw4oYO.Um9JlcX6E7PphX1fnLqe8g2MKjxJvO",
            cep="0123012",
            address="R. Ana Neri, 365",
            district="Vila Metalurgica",
            allow_delivery=True
        )

        retirador3 = Collector(
            name="Bio Coleta de Oleo Usado",
            document="12345560-12",
            email="collector@collector.com",
            telephone="11912345678",
            hashed_password="$2b$12$2UGp20WpjEaU7VJiBw4oYO.Um9JlcX6E7PphX1fnLqe8g2MKjxJvO",
            cep="0123012",
            address="Av. Manuel Velho Moreira, 1148",
            district="Parque Colonial",
            allow_delivery=False
        )

        db.add(doador1)
        db.add(doador2)
        db.add(retirador1)
        db.add(retirador2)
        db.add(retirador3)
        db.commit()

        oil1 = Oil(
            oil_quantity=10,
            cep="0012312",
            district="Vila Prudente",
            address="Rua do Orfanato",
            address_number=109,
            complement="apto 5",
            day_available="sabado",
            telephone="11992391923",
            is_available=True,
            donator=doador1
        )

        oil2 = Oil(
            oil_quantity=20,
            cep="0012312",
            district="Sapopemba",
            address="R. Francesco Usper",
            address_number=20,
            complement="",
            day_available="domingo",
            telephone="11992391923",
            is_available=True,
            donator=doador2
        )

        oil3 = Oil(
            oil_quantity=30,
            cep="0012312",
            district="São Lucas",
            address="rua X",
            address_number=20,
            complement="apto X",
            day_available="quarta-feira",
            telephone="11992391923",
            is_available=False,
            donator=doador3
        )

        oil4 = Oil(
            oil_quantity=40,
            cep="0012312",
            district="Vila Prudente",
            address="rua X",
            address_number=10,
            complement="apto X",
            day_available="sabado",
            telephone="11992391923",
            is_available=True,
            donator=doador4
        )

        db.add(oil1)
        db.add(oil2)
        db.add(oil3)
        db.add(oil4)
        db.commit()

        doador1.oil = oil1
        doador2.oil = oil2
        doador3.oil = oil3
        doador4.oil = oil4
        db.commit()

        oil_collect = OilCollect(
            oil_id=oil3.id,
            day=datetime.date(2024, 1, 10),
            is_collected=False
        )

        oil3.oil_collect = oil_collect
        db.commit()

    finally:
        db.close()
