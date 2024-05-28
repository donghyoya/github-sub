from fastapi import APIRouter, BackgroundTasks, Query, \
    Depends, Request
from typing import List
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import re

from default.config import dbconfig
from default.config.crawlerconfig import get_crawling_driver
from default.utils.urlutils import url_checker

from domain.crawler import service as crawlerService

load_dotenv('.env')

router = APIRouter(
    tags=["crawler"]
    )

def get_db():
    try:
        db = dbconfig.SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/crawl")
async def perform_crawl(background_tasks: BackgroundTasks, url: str, extensions: List[str] = Query(...)):
    # 비동기 작업으로 크롤링 실행
    print("extensions: ",extensions)
    #background_tasks.add_task(crawl_git_repository, background_tasks, url, extensions)
    return {"message": "Crawling started", "url": url, "extensions": extensions}

@router.get("/crawling")
async def start_crawling(url:str, background_tasks: BackgroundTasks, request: Request, db: Session = Depends(get_db)):
    repo = url_checker(url)
    request.session.clear()
    if repo is not None:
        status, value = crawlerService.service_start(username=repo[0], reponame=repo[1], 
                                                   url=url, background_tasks=background_tasks, 
                                                   db=db)
        #CralwerBaseSchema
        session_data = f'username:{value.username} reponame:{value.reponame}'
        print("cralwer router: ",session_data)
        request.session['crawler'] = session_data

        return status
    return {"error": "Invalid repository URL"}