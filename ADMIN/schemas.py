from pydantic import BaseModel 

class CreateUser(BaseModel):
    username: str
    password: str



class User(BaseModel):
    username: str
    password: str
    class Config:
        orm_mode = True 

class UserUpdateRequest(BaseModel):
    new_username: str
    new_password: str 



class Admin(BaseModel):
    username: str
    password: str





