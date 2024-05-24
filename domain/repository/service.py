from sqlalchemy.orm import Session
from sqlalchemy import or_
from .model import Repository
from .schema import RepositorySchema

def create_repository(db: Session, repository: RepositorySchema):
    db_repository = Repository(**repository.dict())
    db.add(db_repository)
    db.commit()
    db.refresh(db_repository)
    return db_repository

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