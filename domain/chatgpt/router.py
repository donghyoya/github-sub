from fastapi import APIRouter, Depends, HTTPException, Body, Query, Header
from . import schema

router = APIRouter(
    tags=["chatgpt"]
)

@router.post("/chat",response_model=schema.ResChat)
async def chatWithGpt(chat: schema.ResChat):
    if(chat == ""):
        raise HTTPException(status_code=400, detail="write anything")    
    