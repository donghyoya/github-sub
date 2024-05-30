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

@router.get("/getSourcode",response_model=List[schema.SourceCodeReadSchema])
def test_getbyrid(request: Request, db: Session = Depends(get_db)):

    session_data = request.session.get('crawler')
    # print(f"sourceCode Session data: {session_data}")

    if session_data:
        data_parts = session_data.split()
        input_username = data_parts[0].split(':')[1]
        input_reponame = data_parts[1].split(':')[1]
        cralwer = CrawlerBaseSchema(username=input_username, reponame=input_reponame)
        cralwer.print()

    return service.get_source_codes_by_repository_id(cralwer, db=db)