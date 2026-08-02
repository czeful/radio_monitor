from database.database import engine
from collections.abc import Generator
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.orm import Session

SessionLocal = sessionmaker(bind=engine, autoflush=True, expire_on_commit=False)


def get_session()-> Generator[Session, None , None]:

    session = SessionLocal()

    try:
        yield session

    finally: 
        session.close()