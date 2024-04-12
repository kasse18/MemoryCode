from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from bot.config import config


SQLALCHEMY_DATABASE_URL = f"postgresql://{config.db.db_user_name}:{config.db.db_user_password}@{config.db.db_host}:{config.db.db_port}/{config.db.db_name}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()