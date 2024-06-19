from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from rest_framework import status
from schemas import *
from models import *
from database import *
from hashing import *

app = FastAPI()
router = APIRouter()

@router.post("/admin/create", status_code=status.HTTP_201_CREATED)
def create_admin(admin: Admin, db: Session = Depends(get_db_admin)):
    user = db.query(AdminModel).filter(AdminModel.username == admin.username).first()

    if user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = get_password_hash(admin.password)
    new_admin = AdminModel(username=admin.username, password=hashed_password)

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return {"message": "Admin created successfully"}

@router.post("/admin")
def admin_login(admin: Admin, db: Session = Depends(get_db_admin)):
    user = db.query(AdminModel).filter(AdminModel.username == admin.username).first()

    if not user or not verify_password(admin.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    return {"message": "Login successful"}

app.include_router(router)