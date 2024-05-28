from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from .model import SourceCode
from .schema import SourceCodeSchema, SourceCodeReadSchema
from typing import List, Optional
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

# SourceCode 데이터중에 rid값을 가진 데이터가 있는지 없는지 확인
def source_code_exists(rid: int, db: Session) -> bool:
    return db.query(SourceCode).filter(SourceCode.rid == rid).first() is not None

# 2. RID에 해당하는 모든 SourceCode 데이터를 가져오는 서비스
def get_all_source_codes_by_rid(rid: int, db: Session) -> List[SourceCode]:
    return db.query(SourceCode).filter(SourceCode.rid == rid).all()



# 3. list[SourceCode]을 sourceName와 path를 통해 업데이트하거나 추가하는 서비스
def add_or_update_source_codes(source_codes: List[SourceCode], db: Session):
    for src in source_codes:
        existing_source_code = db.query(SourceCode).filter(
            and_(SourceCode.sourceName == src.sourceName, SourceCode.path == src.path)
        ).first()

        if existing_source_code:
            # Update existing source code
            existing_source_code.sourceCode = src.sourceCode
            existing_source_code.url = src.url
            existing_source_code.language = src.language
            db.add(existing_source_code)
        else:
            # Add new source code
            db.add(src)
    
    db.commit()