from fastapi import APIRouter, Depends, HTTPException, Body, Query,\
    Request
from . import service, schema
from sqlalchemy.orm import Session
from typing import List

from default.config import dbconfig
from default.schema.cralwerschema import CrawlerBaseSchema


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
def test_getbyrid(request: Request, db: Session = Depends(get_db)):

    session_data = request.session.get('crawler')

    if session_data:
        data_parts = session_data.split()
        username = data_parts[0].split(':')[1]
        reponame = data_parts[1].split(':')[1]
        cralwer = CrawlerBaseSchema(username=username, reponame=reponame)
    

    return service.get_source_codes_by_repository_id(cralwer, db=db)