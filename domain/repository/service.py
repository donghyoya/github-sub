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
    raise NotImplementedError("The function needs to be called with specific type")

def get_repository(db: Session, rid: int):
    return db.query(Repository).filter(Repository.rid == rid).first()

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


@create_repository.register(RepositorySchema)
def create_repository_schema(db: Session, updates: RepositorySchema):
    db_repository = Repository(**updates.dict())
    db.add(db_repository)
    db.commit()
    db.refresh(db_repository)
    return db_repository

@create_repository.register(Repository)
def create_repository_model(db: Session, repository: Repository):
    db.add(repository)
    db.commit()
    db.refresh(repository)
    return repository


@update_repository.register(RepositorySchema)
def update_repository_schema(db: Session, rid: int, updates: RepositorySchema):
    db_repository = db.query(Repository).filter(Repository.rid == rid).first()
    if db_repository:
        for var, value in updates.dict().items():
            if value is not None:
                setattr(db_repository, var, value)
        db.commit()
        return db_repository
    return None

@update_repository.register(Repository)
def update_repository_model(db: Session, rid: int, updates: Repository):
    db_repository = db.query(Repository).filter(Repository.rid == rid).first()
    if db_repository:
        for key, value in vars(updates).items():
            if value is not None:
                setattr(db_repository, key, value)
        db.commit()
        return db_repository
    return None