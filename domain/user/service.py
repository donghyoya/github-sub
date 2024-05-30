from sqlalchemy.orm import Session
from functools import singledispatch
from sqlalchemy import or_
from .model import GithubUser
from .schema import GithubUserSchema, CreateUserSchema
"""
pydantic 으로 받아온 데이터는 api를 통해서 받아오는 경우
내부에서 동작할때는 sqlalchemy로 하는게 훨씬 효과적
"""

def get_user(user_id: int, db: Session):
    return db.query(GithubUser).filter(GithubUser.uid == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(GithubUser).offset(skip).limit(limit).all()

@singledispatch
def create_user(user, db: Session):
    raise NotImplementedError("Unsupported type")

@create_user.register(GithubUser)
def create_user_model(user: GithubUser, db: Session) -> GithubUser:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@create_user.register(CreateUserSchema)
def create_user_schema(user: CreateUserSchema, db: Session) -> GithubUser:
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

@singledispatch
def update_user(user, user_id: int, db: Session) -> GithubUser:
    raise NotImplementedError("Unsupported type")

@update_user.register(GithubUserSchema)
def _(user: GithubUserSchema, db: Session):
    db_user = get_user(db, user.uid)
    if not db_user:
        return None
    for var, value in vars(user).items():
        setattr(user, var, value) if value else None
    db.commit()
    return user

@update_user.register(GithubUser)
def _(user: GithubUser, db: Session):
    db_user = get_user(user.uid, db=db)
    if not db_user:
        return None
    # Assuming GithubUser model object is fully prepared for update
    for key, value in vars(user).items():
        if value is not None:
            setattr(user, key, value)
    db.commit()
    return user