from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///db/db.sqlite', echo=False)


class User(Base):
    __tablename__ = 'user'
    user_id = Column(String, primary_key=True)
    wants_to_subscribe = Column(Boolean)
    wants_to_unsubscribe = Column(Boolean)

    def __init__(self, id_):
        self.user_id = id_
        self.wants_to_subscribe = False
        self.wants_to_unsubscribe = False

    def get_subscribe_status(self):
        if self.wants_to_subscribe is True:
            return True
        if self.wants_to_unsubscribe is True:
            return False


def get_user(user_id):
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    exists_records = [user for user in session.query(User).filter(User.user_id == user_id)]
    if len(exists_records) == 0:
        user = add_user(user_id, session)
    else:
        user = exists_records[0]
    return user, session


def get_all_users():
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    print(session.query(User).all())
    # exists_records = [user for user in session.query(User).filter()]

    session.commit()
    # return exists_records


def add_user(user_id, session):
    user = User(user_id)
    session.add(user)
    return user


def create_table():
    Base.metadata.create_all(engine)
