from crud import *
from routers import auth
from passlib.context import CryptContext
from typing_extensions import Annotated
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import *
from schemas import CreateUser, User
from models import User as UserModel
from passlib.context import CryptContext

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

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def render_login(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/admin.html")
async def render_login(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/index.html")
async def render_login(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})





@app.get("/users/", response_model=List[User])
def get_all_users(db: Session = Depends(get_db)):
    """Fetches all users from the database."""
    users = db.query(UserModel).all()
    return users

@app.get("/users/{username}", response_model=User)
def read_user_api(username: str, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == username).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/create", response_model=User)
def create_user_api(user: CreateUser, db: Session = Depends(get_db)):
    try:
        created_user = UserModel(username=user.username, password=get_password_hash(user.password))
        db.add(created_user)
        db.commit()
        db.refresh(created_user)
        return created_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/users/{username}", response_model=User)
async def update_user_api(username: str, new_username: str, new_password: str, db: Session = Depends(get_db)):
    updated_user = db.query(UserModel).filter(UserModel.username == username).first()
    if updated_user:
        updated_user.username = new_username
        updated_user.password = get_password_hash(new_password)
        db.commit()
        return updated_user
    else:
        raise HTTPException(status_code=404, detail="User not found") 

@app.delete("/users/{username}", response_model=dict)
async def delete_user_api(username: str, db: Session = Depends(get_db)):
    deleted_user = db.query(UserModel).filter(UserModel.username == username).first()
    if deleted_user:
        db.delete(deleted_user)
        db.commit()
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
