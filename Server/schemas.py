from pydantic import BaseModel

class EmployeeCreate(BaseModel):
    username: str
    password: str

class EmployeeResponse(BaseModel):
    username: str

    class Config:
        orm_mode = True
