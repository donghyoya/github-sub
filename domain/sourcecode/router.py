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