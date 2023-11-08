from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models.collector import Collector
from models.donator import Donator

DB_URL = 'sqlite:///oleo-descarte.sqlite3'

engine = create_engine(DB_URL, connect_args={'check_same_thread': False})
sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
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
        donator = Donator(
            email="donator@donator.com",
            name="donator",
            surname="fernandes",
            hashed_password="$2b$12$2UGp20WpjEaU7VJiBw4oYO.Um9JlcX6E7PphX1fnLqe8g2MKjxJvO",
            telephone="11912345678"
        )

        collector = Collector(
            document="12345560-12",
            email="collector@collector.com",
            telephone="11912345678",
            hashed_password="$2b$12$2UGp20WpjEaU7VJiBw4oYO.Um9JlcX6E7PphX1fnLqe8g2MKjxJvO",
            cep="0123012",
            address="aquela rua lá",
            district="aquele bairro lá",
            allow_delivery=True
        )

        db.add(donator)
        db.add(collector)
        db.commit()
    finally:
        db.close()



