from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from schemas import *
from models import *
from database import *

app = FastAPI()
router = APIRouter()

@router.post("/admin")
def admin_login(admin: Admin, db: Session = Depends(get_db_admin)):
    user = db.query(AdminModel).filter(AdminModel.username == admin.username).first()

    if not user or not verify_password(admin.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return {"message": "Login successful"}

app.include_router(router)
