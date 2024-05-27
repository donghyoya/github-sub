from sqlalchemy.orm import Session
from sqlalchemy import or_
from .model import SourceCode
from .schema import SourceCodeSchema, SourceCodeReadSchema
from functools import singledispatch

def get_source_code(db: Session, sid: int):
    return db.query(SourceCode).filter(SourceCode.sid == sid).first()

def get_source_codes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SourceCode).offset(skip).limit(limit).all()

@singledispatch
def create_source_code(source_code, db: Session):
    raise NotImplementedError("Unsupported type")

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

# SourceCodeSchema 타입에 대한 함수
@create_source_code.register(SourceCodeSchema)
def _(source_code: SourceCodeSchema, db: Session):
    db_source_code = SourceCode(**source_code.dict())
    db.add(db_source_code)
    db.commit()
    db.refresh(db_source_code)
    return db_source_code

# SourceCode 모델 인스턴스에 대한 함수
@create_source_code.register(SourceCode)
def _(source_code: SourceCode, db: Session):
    db.add(source_code)
    db.commit()
    db.refresh(source_code)
    return source_code

def get_source_codes_by_repository_id(db: Session, repository_id: int):
    sources = db.query(SourceCode).filter(SourceCode.rid == repository_id).all()
    return [SourceCodeReadSchema.model_validate(sources) for source in sources]
