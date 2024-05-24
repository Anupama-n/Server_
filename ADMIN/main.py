from fastapi import FastAPI, Depends, HTTPException,status
from sqlalchemy.orm import Session
from database import *
from schemas import CreateUser
from crud import *
from routers import auth
from passlib.context import CryptContext
from typing_extensions import Annotated
app = FastAPI()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)



def get_db():
    db = SessionLocalUser()
    try:
        yield db
    finally:
        db.close()
init_db()

app.include_router(auth.router)

@app.post("/users/create")
def create_user_api(username: str, password: str):
    from ADMIN.database import SessionLocalUser

    db = SessionLocalUser()
    try:
        user = create_user(db, username, password)
        return user
    finally:
        db.close()

@app.get("/users/{username}")
def read_user_api(username: str, db: Session = Depends(get_db)):
    db_user = read_user(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.put("/users/{username}")
async def update_user_api(username: str, new_username: str, new_password: str, db: Session = Depends(get_db)):
    updated_user = update_user(db, username, new_username, new_password)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/users/{username}")
async def delete_user_api(username: str, db: Session = Depends(get_db)):
    deleted_user = delete_user(db, username)
    if deleted_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}



