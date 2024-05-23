from sqlalchemy import Column, Integer, String
from database import Base


class User(Base): 
    __tablename__ = "employee"
    username = Column(String, primary_key= True, index = True)
    password = Column (String)

