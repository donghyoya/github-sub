from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from .model import SourceCode
from .schema import SourceCodeSchema, SourceCodeReadSchema
from typing import List, Optional
from functools import singledispatch

from default.utils.redisutils import RepositoryWorkingStatus
from default.schema.cralwerschema import CrawlerBaseSchema
from default.config import dbconfig

from domain.repository.model import Repository

def get_db():
    try:
        db = dbconfig.SessionLocal()
        yield db
    finally:
        db.close()


def get_source_codes_by_session(request: Request):
    db = next(get_db)

    session_data = request.session.get('cralwer')

    if session_data:
        data_parts = session_data.split()
        input_username = data_parts[0].split(':')[1]
        input_reponame = data_parts[1].split(':')[1]
        input_host = data_parts[2].split(':')[1]

    redis_data = RepositoryWorkingStatus.from_redis(input_username, input_reponame)
    

    


def get_source_codes_by_repository_id(crawler: CrawlerBaseSchema, db: Session)-> List[SourceCodeReadSchema]:

    redis_data = RepositoryWorkingStatus.from_redis(crawler.username, crawler.reponame)
    
    if not redis_data:
        raise HTTPException(status_code=404, detail="Repository status not found in Redis")
    
    # print("redis_data rid: ",redis_data.get_repoid())
    
    sources = db.query(SourceCode).filter(SourceCode.rid == redis_data.get_repoid()).all()

    returnlist = [SourceCodeReadSchema.model_validate(source) for source in sources]
    print(returnlist)
    return returnlist


'''
============crud===========
'''

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

# SourceCode 데이터중에 rid값을 가진 데이터가 있는지 없는지 확인
def source_code_exists(rid: int, db: Session) -> bool:
    return db.query(SourceCode).filter(SourceCode.rid == rid).first() is not None

# 2. RID에 해당하는 모든 SourceCode 데이터를 가져오는 서비스
def get_all_source_codes_by_rid(rid: int, db: Session) -> List[SourceCode]:
    return db.query(SourceCode).filter(SourceCode.rid == rid).all()


# 3. list[SourceCode]을 sourceName와 path를 통해 업데이트하거나 추가하는 서비스
def add_or_update_source_codes(source_codes: List[SourceCode],repository: Repository, db: Session) -> List[SourceCode]:
    updated_or_added = []
    
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
            updated_or_added.append(existing_source_code)
        else:
            src.rmstate=True
            src.rid = repository.rid
            src.repository = repository
            # Add new source code
            db.add(src)
            updated_or_added.append(src)
    
    db.commit()
    return updated_or_added

'''
소스코드 db에 '적재'만하는 소스
'''
def add_source_codes(source_codes: List[SourceCode], repository: Repository, db: Session) -> List[SourceCode]:
    added = []

    for src in source_codes:
        if(len(src.sourceCode) >= 65534):
            src.sourceCode("too long")
        src.rmstate = True
        src.rid = repository.rid
        src.repository = repository
        db.add(src)
        added.append(src)
    
    db.commit()
    return added

'''
없어진 소스코드 삭제(status를 False로 변환)
'''
def update_rmstate_for_missing_sids(missing_sids: List[int], db: Session):
    if not missing_sids:
        return
    
    # Update rmstate for SourceCode entries with sids in missing_sids
    db.query(SourceCode).filter(SourceCode.sid.in_(missing_sids)).update({"rmstate": False}, synchronize_session=False)
    db.commit()