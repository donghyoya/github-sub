from fastapi import APIRouter, Depends, HTTPException, \
    Body, Query, status, Request
from . import service, schema
from sqlalchemy.orm import Session
from typing import List
from redis import Redis

from default.config import dbconfig
from default.config.aiconfig import AiConfig
from default.config.redisdbconfig import get_redis

from default.schema.cralwerschema import CrawlerBaseSchema
from .service import create_ai_result

router = APIRouter(
    tags=["airesult"]
)

def get_db():
    try:
        db = dbconfig.SessionLocal()
        yield db
    finally:
        db.close()
        
def get_ai():
    return AiConfig.get_instance()  

def get_redis_db():
    return get_redis


@router.post("/chat", response_model=schema.AiResultBaseSchema)
async def perform_text_completion(prompt: str, request: Request, ai_config: AiConfig = Depends(get_ai), db: Session = Depends(get_db)):
    
    session_data = request.session.get('crawler')
    # print(f"ai_result Session data: {session_data}")

    if session_data:
        data_parts = session_data.split()
        username = data_parts[0].split(':')[1]
        reponame = data_parts[1].split(':')[1]
        cralwer = CrawlerBaseSchema(username=username, reponame=reponame)
    try:
        completion = ai_config.chat(prompt=prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    ai_setting = schema.AiSettingSchema(model=ai_config.output_model, answer=completion)
    ai_result =service.insertOrUpdateAi(airesult=ai_setting, crawler=cralwer, db=db)
    return ai_result

@router.post("/airesults/",response_model=schema.AiResultSchema, 
             status_code = status.HTTP_200_OK)
def create_ai_resutl(ai_result: schema.AiResultSchema, db: Session = Depends(get_db)):
    return create_ai_result(db=db, ai_result= ai_result)

@router.get("/airesults/{aid}", response_model=schema.AiResultSchema)
def read_result(aid: int, db: Session = Depends(get_db)):
    db_ai_result = service.get_ai_result(db, aid)
    if db_ai_result is None:
        raise HTTPException(status_code=404, detail="AI result not found")
    return db_ai_result

@router.put("/airesults/{aid}", response_model=schema.AiResultSchema)
def update_result(aid: int, ai_result: schema.AiResultSchema, db: Session = Depends(get_db)):
    db_ai_result = service.update_ai_result(db, aid, ai_result)
    if db_ai_result is None:
        raise HTTPException(status_code=404, detail="AI result not found")
    return db_ai_result

@router.delete("/airesults/{aid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_result(aid: int, db: Session = Depends(get_db)):
    if not service.delete_ai_result(db, aid):
        raise HTTPException(status_code=404, detail="AI result not found")
    return {"message": "AI result deleted successfully"}