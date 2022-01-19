from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import DB_PATH, CLIENT_DB_PATH

engine = create_engine(f'sqlite:///{DB_PATH}', echo=True)
SessionLocal = sessionmaker(engine, expire_on_commit=False)


client_engine = create_engine(f'sqlite:///{CLIENT_DB_PATH}', echo=True)
ClientSessionLocal = sessionmaker(client_engine, expire_on_commit=False)



@contextmanager
def get_session(session):
    db_adapter = None
    try:
        db_adapter = session()
        yield db_adapter
    finally:
        if db_adapter:
            db_adapter.close()


