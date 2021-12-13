import datetime
import os
from pathlib import Path
from sqlalchemy import create_engine, Column, ForeignKey, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.testing.schema import Table

from settings import DB_PATH

Base = declarative_base()

engine = create_engine(f'sqlite:///{DB_PATH}', echo=True)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(100), unique=True, nullable=False)
    info = Column(String(255))
    contacts = relationship('UserContacts')

    def __init__(self, nickname, info=None):
        self.nickname = nickname
        self.info = info

    def __repr__(self):
        return f'<User(id={self.id}, nickname={self.nickname}, info={self.info}>'


class UserContacts(Base):
    __tablename__ = 'user_contacts'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    user_to_save_name = Column(String)

    def __init__(self, user_id, user_name_to_save):
        self.user_id = user_id
        self.user_to_save_name = user_name_to_save

    def __repr__(self):
        return f'<UserContact(id={self.id}, user_id={self.user_id}, user_to_save_name={self.user_to_save_name}>'


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
