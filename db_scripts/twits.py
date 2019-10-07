from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_scripts.following import Following
Base = declarative_base()
engine = create_engine('sqlite:///db/db.sqlite', echo=False)


class Twit(Base):
    __tablename__ = 'twit'
    twit_id = Column(String, primary_key=True)
    following_id = Column(String, ForeignKey(Following.following_id), primary_key=True)
    twit_text = Column(String)

    def __init__(self, twit_id, following_id, twit_text):
        self.twit_id = twit_id
        self.following_id = following_id
        self.twit_text = twit_text


def get_user_twits(following_id):
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    exists_records = [twit for twit in session.query(Twit).filter(Twit.following_id == following_id)]

    session.commit()
    return exists_records


def __add_twit(twit_id, following_id, twit_text, session):
    twit = Twit(twit_id, following_id, twit_text)
    session.add(twit)


def add_twits(following_id, twits):
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()

    for twit_id, twit_text in twits.items():
        __add_twit(twit_id, following_id, twit_text, session)

    session.commit()


def create_table():
    Base.metadata.create_all(engine)
