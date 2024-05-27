from fastapi import APIRouter, BackgroundTasks, Query, \
    Depends
from typing import List
from dotenv import load_dotenv
from sqlalchemy.orm import Session
import re

from default.config import dbconfig

from domain.crawler.crawler import gitCrawler
from default.config.crawlerconfig import get_crawling_driver
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

def crawl_git_repository(background_tasks: BackgroundTasks, url: str, extensions: list):
    try:
        driver = get_crawling_driver()
        crawler = gitCrawler(driver)
        crawler.start_crawl(url, extensions)
        src_files = crawler.get_src_files()
        crawler.close()
        # for src in src_files:
        #     print(src.src)
        return src_files
    except Exception as e:
        print(e)

@router.get("/crawl")
async def perform_crawl(background_tasks: BackgroundTasks, url: str, extensions: List[str] = Query(...)):
    # 비동기 작업으로 크롤링 실행
    print("extensions: ",extensions)
    background_tasks.add_task(crawl_git_repository, background_tasks, url, extensions)
    return {"message": "Crawling started", "url": url, "extensions": extensions}

@router.get("/crawling")
async def start_crawling(url:str , db: Session = Depends(get_db)):
    repo = url_checker(url)
    if repo is not None:
        repository = crawlerService.start_crawling()

# if __name__ == "__main__":
#     driver = get_crawling_driver()
#     crawler = GitCrawler(driver)
#     # url = ""
#     url = "https://github.com/donghyoya/github-sub"
#     crawler.start_crawl(url, ["py"])
#     src_files = crawler.get_src_files()
#     crawler.close()
#     if src_files is not None:
#         for src in src_files:
#             print(src.title)
#     # src_f

# utils
REPO_URL_PATTERN = r'https?://github.com/[a-zA-Z0-9]+/[a-zA-Z0-9_-]+'
REPO_NAME_PATTERN = r'github.com/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)'

def url_checker(url: str):
    """
    url이 github url인가 체크
    """
    if re.match(REPO_URL_PATTERN, url):
        return re.findall(REPO_NAME_PATTERN, url)[0]
    else:
        return None