from sqlalchemy import create_engine, Column, ForeignKey, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from settings import CLIENT_DB_PATH

Base = declarative_base()

engine = create_engine(f'sqlite:///{CLIENT_DB_PATH}', echo=True)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    nickname = Column(String(100), unique=True, nullable=False)
    info = Column(String(255))
    messages = relationship('UserMessages')

    def __init__(self, nickname, info=None):
        self.nickname = nickname
        self.info = info

    def __repr__(self):
        return f'<User(id={self.id}, nickname={self.nickname}, info={self.info}>'


class UserMessages(Base):
    __tablename__ = 'user_messages'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    message = Column(String)

    def __init__(self, user_id, message):
        self.user_id = user_id
        self.message = message

    def __repr__(self):
        return f'UserMessage<id={self.id}, user_id={self.user_id}, message={self.message}>'


Base.metadata.create_all(engine)
