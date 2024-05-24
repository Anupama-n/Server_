from pydantic import BaseModel 

class CreateUser(BaseModel):
    username: str
    password: str


class Admin(BaseModel):
    username: str
    password: str





