import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . import config

# Postgres
DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "500"))
WEB_CONCURRENCY = int(os.getenv("WEB_CONCURRENCY", "8"))
POOL_SIZE = max(DB_POOL_SIZE // WEB_CONCURRENCY, 5)

engine = create_engine(config.SQLALCHEMY_DATABASE_URI,
                       client_encoding='utf8',
                       pool_pre_ping=True,
                       pool_size=POOL_SIZE,
                       max_overflow=0,
                       pool_timeout=120,
                       pool_recycle=3600)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as exc:
        db.rollback()
        raise exc
    finally:
        db.close()
