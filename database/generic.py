from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from setting.config import get_settings
from models.user import User
from models.item import Item

settings = get_settings()

engine = create_engine(
    settings.database_url,
    echo=True,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine, tables=[User.__table__, Item.__table__])
    
def get_db():
    return SessionLocal()