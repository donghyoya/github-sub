from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from functools import singledispatch

from .model import AiResult
from .schema import AiResultSchema, AiSettingSchema, \
    AiResultBaseSchema, AiResultBaseSchema

from default.utils.redisutils import RepositoryWorkingStatus

from domain.repository.service import get_repository
from default.schema.cralwerschema import CrawlerBaseSchema


def insertOrUpdateAi(airesult: AiSettingSchema, crawler: CrawlerBaseSchema, db: Session) -> AiResultBaseSchema:
    
    redis_data = RepositoryWorkingStatus.from_redis(crawler.username, crawler.reponame)
    
    if not redis_data:
        raise HTTPException(status_code=404, detail="Repository status not found in Redis")

    repository = get_repository(rid=redis_data.get_repoid(),db=db)
    ai_result_insert_db = AiResult(model=airesult.model, answer=airesult.answer,
                                   score=50, rid=repository.rid, repository=repository)
    ai_resultdb = create_ai_result(ai_result_insert_db, db)

    return AiResultBaseSchema.model_validate(ai_resultdb)

'''
====crud=====
'''

@singledispatch
def create_ai_result(ai_result, db: Session):
    raise NotImplementedError("Unsupported type")

@create_ai_result.register(AiResultSchema)
def _(ai_result: AiResultSchema, db: Session):
    db_ai_result = AiResult(**ai_result.model_dump())
    db.add(db_ai_result)
    db.commit()
    db.refresh(db_ai_result)
    return db_ai_result

@create_ai_result.register(AiResult)
def _(ai_result: AiResult, db: Session):
    print('running in create_ai')
    db.add(ai_result)
    db.commit()
    db.refresh(ai_result)
    return ai_result

def get_ai_result(db: Session, aid: int):
    return db.query(AiResult).filter(AiResult.aid == aid).first()


@singledispatch
def update_ai_result(updates, db: Session):
    raise NotImplementedError("Unsupported type")

@update_ai_result.register(AiResultBaseSchema)
def _(updates: AiResultBaseSchema, db: Session):
    db_ai_result = db.query(AiResult).filter(AiResult.aid == updates.aid).first()
    if db_ai_result:
        for var, value in updates.dict().items():
            setattr(db_ai_result, var, value) if value else None
        db.commit()
        return db_ai_result
    return None

@update_ai_result.register(AiResult)
def _(updateAiresult: AiResult, db: Session):
    db_ai_result=get_ai_result(aid=updateAiresult.aid, db=db)
    if db_ai_result:
        for key, value in vars(updateAiresult).items():
            if value is not None:
                setattr(db_ai_result, key, value)
        db.commit()
        return db_ai_result
    return None

def delete_ai_result(db: Session, aid: int):
    db_ai_result = db.query(AiResult).filter(AiResult.aid == aid).first()
    if db_ai_result:
        db.delete(db_ai_result)
        db.commit()
        return True
    return False


def get_first_ai_result_by_rid(rid: int, db: Session) -> AiResult:
    return db.query(AiResult).filter(AiResult.rid == rid).first()

'''
def get_matching_ai_results(ai_reslt: AiResult, repostory:Repository,db: Session):
    results = db.query(ai_reslt).join(
        repostory,
        and_(
            AiResult.rid == Repository.rid,
            AiResult.repoTh == Repository.connectCnt
        )
    ).first()
    return results
'''