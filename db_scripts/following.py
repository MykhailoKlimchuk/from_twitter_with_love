from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_scripts.user import User
# from scraper.twit_scraper import check_following_exists


Base = declarative_base()
engine = create_engine('sqlite:///db/db.sqlite', echo=False)


class Following(Base):
    __tablename__ = 'following'
    following_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey(User.user_id), primary_key=True)

    def __init__(self, following_id, user_id):
        self.following_id = following_id
        self.user_id = user_id


def get_user_followings(user_id):
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    exists_records = [twit for twit in session.query(Following).filter(Following.user_id == user_id)]

    session.commit()
    return exists_records


def get_following(following_id, user_id, session):
    exists_records = [twit for twit in session.query(Following).filter(Following.user_id == user_id,
                                                                       Following.following_id == following_id)]
    return exists_records


def get_following_by_following_id(following_id):
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()

    exists_records = [twit for twit in session.query(Following).filter(Following.following_id == following_id)]
    session.commit()

    return exists_records


def add_following(following_id, user_id, session):
    exists_records = get_following(following_id, user_id, session)

    if len(exists_records) != 0:
        return

    twit = Following(following_id, user_id)
    session.add(twit)


def del_following(following_id, user_id, session):
    exists_records = get_following(following_id, user_id, session)
    if len(exists_records) == 0:
        return False

    for following in exists_records:
        session.delete(following)
    return True


def create_table():
    Base.metadata.create_all(engine)
