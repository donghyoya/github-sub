from sqlalchemy.orm import Session
from sqlalchemy import or_
from .model import GithubUser, CreateUserSchema

def get_user(db: Session, user_id: int):
    return db.query(GithubUser).filter(GithubUser.uid == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(GithubUser).offset(skip).limit(limit).all()

def create_user(db: Session, user: CreateUserSchema):
    db_user = GithubUser(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: CreateUserSchema):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    for var, value in vars(user).items():
        setattr(db_user, var, value) if value else None
    db.commit()
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
