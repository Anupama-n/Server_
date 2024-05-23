from sqlalchemy.orm import Session
from models import User
from schemas import *
from hashing import get_password_hash

def create_user(db: Session, username: str, password: str):
    hashed_password = get_password_hash(password)
    db_user = User(username=username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def read_user(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()



def update_user(db: Session, username: str, new_username: str, new_password: str) -> User:
    user = db.query(User).filter(User.username == username).first()
    if user:
        user.username = new_username
        user.password = get_password_hash(new_password) 
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, username: str) -> User:
    user = db.query(User).filter(User.username == username).first()
    if user:
        db.delete(user)
        db.commit()
    return user