from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from fastapi import Depends
from typing_extensions import Annotated
import os

# Load environment variables from the .env file
load_dotenv()

# Read the database URLs from the environment variables
SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
SQLALCHEMY_DATABASE_VEHICLE = os.getenv("SQLALCHEMY_DATABASE_VEHICLE")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("SQLALCHEMY_DATABASE_URL is not set in the environment variables")

if not SQLALCHEMY_DATABASE_VEHICLE:
    raise ValueError("SQLALCHEMY_DATABASE_VEHICLE is not set in the environment variables")


engine_employee = create_engine(SQLALCHEMY_DATABASE_URL)
engine_vehicle = create_engine(SQLALCHEMY_DATABASE_VEHICLE)

SessionLocalUser = sessionmaker(autocommit=False, autoflush=False, bind=engine_employee)
SessionLocalVehicle = sessionmaker(autocommit=False, autoflush=False, bind=engine_vehicle)

Base = declarative_base()

# Initialize the database tables
def init_db():
    import models 
    Base.metadata.create_all(bind=engine_employee)
    Base.metadata.create_all(bind=engine_vehicle)

def get_db_user():
    db_user = SessionLocalUser()
    try:
        yield db_user
    finally:
        db_user.close()

def get_db_vehicle():
    db_vehicle = SessionLocalVehicle()
    try:
        yield db_vehicle
    finally:
        db_vehicle.close()
