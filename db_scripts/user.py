from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///db/db.sqlite', echo=True)


class User(Base):
    __tablename__ = 'user'
    id = Column(String, primary_key=True)
    wants_to_subscribe = Column(String)
    wants_to_unsubscribe = Column(String)

    def __init__(self, id_):
        self.id = id_
        self.wants_to_subscribe = False
        self.wants_to_unsubscribe = False


def create_table():
    print(create_table)
    Base.metadata.create_all(engine)
