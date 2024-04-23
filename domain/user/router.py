from fastapi import APIRouter, Depends, HTTPException,\
    Body, Query, Request
from . import service, schema
from sqlalchemy.orm import Session
from typing import List
from default.config import dbconfig

router = APIRouter(
    tags=["user"]
)

def get_db():
    db = None
    try:
        db = dbconfig.SessionLocal()
        yield db
    finally:
        if db:
            db.close()

@router.get("/testredis")
def getRedis(request: Request, db: Session = Depends(get_db)):
    print(request)
    return "test"