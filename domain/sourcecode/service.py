from sqlalchemy.orm import Session
from sqlalchemy import or_
from .model import SourceCode
from .schema import SourceCodeSchema

def get_source_code(db: Session, sid: int):
    return db.query(SourceCode).filter(SourceCode.sid == sid).first()

def get_source_codes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SourceCode).offset(skip).limit(limit).all()

def create_source_code(db: Session, source_code: SourceCodeSchema):
    db_source_code = SourceCode(**source_code.dict())
    db.add(db_source_code)
    db.commit()
    db.refresh(db_source_code)
    return db_source_code

def update_source_code(db: Session, sid: int, updates: SourceCodeSchema):
    db_source_code = db.query(SourceCode).filter(SourceCode.sid == sid).first()
    if db_source_code:
        for var, value in updates.dict().items():
            setattr(db_source_code, var, value) if value else None
        db.commit()
        return db_source_code
    return None

def delete_source_code(db: Session, sid: int):
    db_source_code = db.query(SourceCode).filter(SourceCode.sid == sid).first()
    if db_source_code:
        db.delete(db_source_code)
        db.commit()
        return True
    return False
