from fastapi import APIRouter, BackgroundTasks, Query
from typing import List
from dotenv import load_dotenv

from default.config.crawlerconfig import get_crawling_driver
from domain.crawler.crawler import GitCrawler

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

@router.get("/crawl")
async def perform_crawl(background_tasks: BackgroundTasks, url: str, extensions: List[str] = Query(...)):
    # 비동기 작업으로 크롤링 실행
    background_tasks.add_task(crawl_git_repository, background_tasks, url)
    return {"message": "Crawling started", "url": url, "extensions": extensions}


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