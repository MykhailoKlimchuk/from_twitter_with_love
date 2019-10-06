from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///db/db.sqlite', echo=False)


class User(Base):
    __tablename__ = 'user'
    id = Column(String, primary_key=True)
    wants_to_subscribe = Column(String)
    wants_to_unsubscribe = Column(String)

    def __init__(self, id_):
        self.id = id_
        self.wants_to_subscribe = False
        self.wants_to_unsubscribe = False

    def subscribe(self):
        self.wants_to_subscribe = True
        self.wants_to_unsubscribe = False

    def unsubscribe(self):
        self.wants_to_subscribe = False
        self.wants_to_unsubscribe = True

    def get_subscribe_status(self):
        if self.wants_to_subscribe is True:
            return True
        if self.wants_to_unsubscribe is True:
            return False

    def process_subscribe_data(self, subscribe_id):
        if self.get_subscribe_status() is True:
            print(f'subscribe {subscribe_id}')
        else:
            print(f'unsubscribe {subscribe_id}')


def get_user(user_id):
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    exists_records = [game for game in session.query(User).filter(User.id == user_id)]
    if len(exists_records) == 0:
        print(111)
        user = add_user(user_id, session)
    else:
        print(222)

        user = exists_records[0]
    session.commit()
    return user


def add_user(user_id, session):
    user = User(user_id)
    session.add(user)
    return user


def create_table():
    print(create_table)
    Base.metadata.create_all(engine)
