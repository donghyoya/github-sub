from sqlalchemy.orm import Session
from functools import singledispatch
from sqlalchemy import or_
from .model import GithubUser
from .schema import GithubUserSchema, CreateUserSchema

def get_user(db: Session, user_id: int):
    return db.query(GithubUser).filter(GithubUser.uid == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(GithubUser).offset(skip).limit(limit).all()

@singledispatch
def update_user(db: Session, user_id: int, user) -> GithubUser:
    raise NotImplementedError("Unsupported type")

@singledispatch
def create_user(db: Session, user) -> GithubUser:
    raise NotImplementedError("Unsupported type")

# GithubUser 모델 인스턴스에 대한 함수
@create_user.register(GithubUser)
def _(db: Session, user: GithubUser) -> GithubUser:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# CreateUserSchema 스키마 인스턴스에 대한 함수
@create_user.register(CreateUserSchema)
def _(db: Session, user: CreateUserSchema) -> GithubUser:
    db_user = GithubUser(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

def get_user_by_username(db: Session, username: str) -> GithubUser:
    return db.query(GithubUser).filter(GithubUser.username == username).first()

@update_user.register(CreateUserSchema)
def _(db: Session, user_id: int, user: CreateUserSchema):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    for var, value in vars(user).items():
        setattr(db_user, var, value) if value else None
    db.commit()
    return db_user

@update_user.register(GithubUser)
def _(db: Session, user_id: int, user: GithubUser):
    db_user = db.query(GithubUser).filter(GithubUser.uid == user_id).first()
    if not db_user:
        return None
    # Assuming GithubUser model object is fully prepared for update
    for key, value in vars(user).items():
        if value is not None:
            setattr(db_user, key, value)
    db.commit()
    return db_user