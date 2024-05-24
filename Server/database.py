from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from fastapi import  Depends
from typing_extensions import Annotated
import os

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")

engine_employee = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocalUser = sessionmaker(autocommit=False, autoflush=False, bind=engine_employee)

Base = declarative_base()

def init_db():

    Base.metadata.create_all(bind= engine_employee)

def get_db_user():
    db_user = SessionLocalUser()
    try:
        yield db_user
    finally: 
        db_user.close()