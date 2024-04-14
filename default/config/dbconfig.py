from sqlalchemy import create_engine

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker, Session

from dotenv import load_dotenv
import os

load_dotenv('.env.local')

DATABASE_URL = os.getenv("DATABASE_URL")

session = Session

# DATABASE_URL = "postgresql://postgres:0814@localhost:5432/postgres"
engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()