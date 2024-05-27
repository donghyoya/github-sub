from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from functools import singledispatch

from .model import AiResult
from .schema import AiResultSchema, AiSettingSchema

from domain.repository.model import Repository
from domain.repository.service import get_repository


def insertOrUpdateAi(airesult: AiSettingSchema, rid:int, db: Session):
    repository = get_repository(rid=rid,db=db)

    ai_result_insert_db = AiResult(model=airesult.model, answer=airesult.answer,
                                   score=50, rid=rid, repository=repository)
    if repository is None:
        create_ai_result

    
    

'''
====crud=====
'''

@singledispatch
def create_ai_result(ai_result, db: Session):
    raise NotImplementedError("Unsupported type")



def get_ai_result(db: Session, aid: int):
    return db.query(AiResult).filter(AiResult.aid == aid).first()


@singledispatch
def update_ai_result(updates, aid: int, db: Session):
    raise NotImplementedError("Unsupported type")



def delete_ai_result(db: Session, aid: int):
    db_ai_result = db.query(AiResult).filter(AiResult.aid == aid).first()
    if db_ai_result:
        db.delete(db_ai_result)
        db.commit()
        return True
    return False
