from functools import singledispatch
from sqlalchemy.orm import Session
from sqlalchemy import or_
from .model import Repository
from .schema import RepositorySchema

# create_repository 함수 오버로딩
@singledispatch
def create_repository(db: Session, repository):
    raise NotImplementedError("Unsupported type")

# update_repository 함수 오버로딩
@singledispatch
def update_repository(db: Session, rid: int, updates):
    raise NotImplementedError("Unsupported type")

def get_repository(db: Session, rid: int):
    return db.query(Repository).filter(Repository.rid == rid).first()

def update_repository(db: Session, rid: int, updates: RepositorySchema):
    db_repository = db.query(Repository).filter(Repository.rid == rid).first()
    if db_repository:
        for var, value in updates.dict().items():
            setattr(db_repository, var, value) if value else None
        db.commit()
        return db_repository
    return None

def delete_repository(db: Session, rid: int):
    db_repository = db.query(Repository).filter(Repository.rid == rid).first()
    if db_repository:
        db.delete(db_repository)
        db.commit()
        return True
    return False

def get_repository_by_name_and_guid(db: Session, repo_name: str, guid: int):
    repository = db.query(Repository).filter(
        Repository.repoName == repo_name,
        Repository.guid == guid
    ).first()
    return repository


@create_repository.register
def _(db: Session, repository: RepositorySchema):
    db_repository = Repository(**repository.dict())
    db.add(db_repository)
    db.commit()
    db.refresh(db_repository)
    return db_repository

@create_repository.register(Repository)
def _(db: Session, repository: Repository):
    db.add(repository)
    db.commit()
    db.refresh(repository)
    return repository


@update_repository.register
def _(db: Session, rid: int, updates: RepositorySchema):
    db_repository = db.query(Repository).filter(Repository.rid == rid).first()
    if db_repository:
        for var, value in updates.dict().items():
            setattr(db_repository, var, value) if value else None
        db.commit()
        return db_repository
    return None

@update_repository.register(Repository)
def _(db: Session, rid: int, updates: Repository):
    db_repository = db.query(Repository).filter(Repository.rid == rid).first()
    if db_repository:
        for key, value in vars(updates).items():
            setattr(db_repository, key, value) if value is not None else None
        db.commit()
        return db_repository
    return None