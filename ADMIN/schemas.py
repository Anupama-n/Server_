from pydantic import BaseModel 

class CreateUser(BaseModel):
    username: str
    password: str



class User(BaseModel):
    username: str
    password: str
    class Config:
        orm_mode = True  



class Admin(BaseModel):
    username: str
    password: str





