from fastapi import APIRouter, Depends, HTTPException, Body, Query, status
from . import service, schema
from sqlalchemy.orm import Session
from typing import List
from default.config import dbconfig

router = APIRouter(
    tags=["airesult"]
)

def get_db():
    try:
        db = dbconfig.SessionLocal()
        yield db
    finally:
        db.close()

@router.post("/airesults/",response_model=schema.AiResultSchema, 
             status_code = status.HTTP_200_OK)
def create_ai_resutl(ai_result: schema.AiResultSchema, db: Session = Depends(get_db)):
    return create_ai_resutl(db=db, ai_result= ai_result)
