from fastapi import APIRouter, Depends, HTTPException, Body, Query
from . import service, schema
from sqlalchemy.orm import Session
from typing import List

from default.config import dbconfig


router = APIRouter(
    tags=["sourcecode"]
)

def get_db():
    try:
        db = dbconfig.SessionLocal()
        yield db
    finally:
        db.close()

@router.get("/getbyrid/{rid}",response_model=List[schema.SourceCodeReadSchema])
def test_getbyrid(rid: int, db: Session = Depends(get_db)):
    return service.get_source_codes_by_repository_id(repository_id=rid, db=db)