from sqlalchemy import Column, Integer, String
from database import Base
from passlib.context import CryptContext

class Employee(Base): 
    __tablename__ = "employee"
    username = Column(String, primary_key= True, index = True)
    password = Column (String)