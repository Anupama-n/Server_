from sqlalchemy import Column, Integer, String
from database import Base
from passlib.context import CryptContext
from hashing import bcrypt_context

class User(Base): 
    __tablename__ = "employee"
    username = Column(String, primary_key= True, index = True)
    password = Column (String)

class AdminModel(Base):
    __tablename__ = 'admin'
    username = Column(String, primary_key=True, index=True)
    password = Column(String)

def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)