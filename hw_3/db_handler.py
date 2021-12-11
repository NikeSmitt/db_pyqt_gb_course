import datetime
import os
from pathlib import Path
from sqlalchemy import create_engine, Column, ForeignKey, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
db_path = 'main.db'


engine = create_engine(f'sqlite:///{db_path}', echo=True)


class User(Base):

    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(100), unique=True)
    info = Column(String(255))

    def __init__(self, nickname, info=None):
        self.nickname = nickname
        self.info = info

    def __repr__(self):
        return f'<User(id={self.id}, nickname={self.nickname}, info={self.info}>'


class UserHistory(Base):

    __tablename__ = 'user_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    login_time = Column(DateTime)

    def __init__(self, user_id, login_time=None):
        self.user_id = user_id
        self.login_time = login_time if login_time else datetime.datetime.now()

    def __repr__(self):
        return f'<UserHistory(id={self.id}, user_id={self.user_id}, login_time={self.login_time}>'


Base.metadata.create_all(engine)


