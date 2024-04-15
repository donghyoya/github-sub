from sqlalchemy.orm import Session
from sqlalchemy import or_
from .model import AiResult
from .schema import AiResultSchema


def create_ai_result(db: Session, ai_result: AiResultSchema):
    db_ai_result = AiResult(**ai_result.dict())
    db.add(db_ai_result)
    db.commit()
    db.refresh(db_ai_result)
    return db_ai_result

def get_ai_result(db: Session, aid: int):
    return db.query(AiResult).filter(AiResult.aid == aid).first()

def update_ai_result(db: Session, aid: int, updates: AiResultSchema):
    db_ai_result = db.query(AiResult).filter(AiResult.aid == aid).first()
    if db_ai_result:
        for var, value in updates.dict().items():
            setattr(db_ai_result, var, value) if value else None
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
