from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import jwt
import os
from models import Employee
from database import get_db_user
from schemas import EmployeeCreate

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv('SECRET_KEY'), algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def login(employee: EmployeeCreate, db: Session = Depends(get_db_user)):
    db_employee = db.query(Employee).filter(Employee.username == employee.username).first()

    if not db_employee:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not bcrypt_context.verify(employee.password, db_employee.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": employee.username}, expires_delta=access_token_expires
    )
    return {"message": "Login successful", "access_token": access_token, "token_type": "bearer"}

def read_protected(token: str = Depends(verify_token)):
    return {"message": "This is a protected route", "user": token["sub"]}
