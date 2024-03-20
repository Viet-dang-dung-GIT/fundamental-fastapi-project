from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"


# SQL ALCHEMY "ENGINE"
engine = create_engine(
    # connect_args only need with sqlite not need other database
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# class SessionLocal actually database session if we create instance SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# later we will inherit from this class Base to create each models database or classes
Base = declarative_base()

