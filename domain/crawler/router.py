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

def crawl_git_repository(background_tasks: BackgroundTasks, url: str):
    try:
        driver = get_crawling_driver()
        crawler = GitCrawler(driver)
        crawler.start_crawl(url)
        src_files = crawler.get_src_files()
        crawler.close()
        # for src in src_files:
        #     print(src.src)
        return src_files
    except Exception as e:
        print(e)
        
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
        session_data = f'username:{value.username} reponame:{value.reponame} host:{request.client.host}'
        # print("cralwer router: ",session_data)
        request.session['crawler'] = session_data

        return status
    return {"error": "Invalid repository URL"}


if __name__ == "__main__":
    driver = get_crawling_driver()
    crawler = GitCrawler(driver)
    # url = ""
    url = "https://github.com/donghyoya/github-sub"
    crawler.start_crawl(url)
    src_files = crawler.get_src_files()
    crawler.close()
    if src_files is not None:
        for src in src_files:
            print(src.title)
    # src_f
