from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from fastapi import  Depends
from typing_extensions import Annotated
import os

load_dotenv()


SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
SQLALCHEMY_DATABASE_ADMIN = os.getenv("SQLALCHEMY_DATABASE_ADMIN")

engine_admin = create_engine(SQLALCHEMY_DATABASE_ADMIN)
engine_user = create_engine(SQLALCHEMY_DATABASE_URL)
 
SessionLocalAdmin = sessionmaker(autocommit=False, autoflush=False, bind=engine_admin)
SessionLocalUser = sessionmaker(autocommit=False, autoflush=False, bind=engine_user)
def get_db_admin():
    db_admin = SessionLocalAdmin()
    try:
        yield db_admin
    finally:
        db_admin.close()

db_dependency = Annotated[Session, Depends(get_db_admin)]

Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind= engine_user)
    Base.metadata.create_all(bind= engine_admin)