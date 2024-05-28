from fastapi import BackgroundTasks, HTTPException
from sqlalchemy.orm import Session

from default.config.crawlerconfig import get_crawling_driver
from default.utils.redisutils import WorkStatus, load_status, save_status, RepositoryWorkingStatus

from .crawler import GitCrawler
from .OrmConverter import conv2orm
from .schema import CrawlerBaseSchema
from domain.user.model import GithubUser
from domain.user import service as GithubUserService
from domain.repository.model import Repository
from domain.repository import service as RepositoryService
from domain.sourcecode.model import SourceCode
from domain.sourcecode import service as SourceCodeService


def service_start(username: str, reponame: str, url: str, 
                  background_tasks: BackgroundTasks , db: Session)->CrawlerBaseSchema:
    
    gitUser = GithubUserService.get_user_by_username(db, username)
        
        # gitUser가 None인 경우 새로운 사용자를 생성
    if gitUser is None:
        gitUser = GithubUser(username=username, site=url, connectCnt=1, follower=0, following=0)
        gitUser = GithubUserService.create_user(gitUser, db)
    else:
        gitUser.connectCnt += 1
        GithubUserService.update_user(gitUser, db)

    # 이제 gitUser는 반드시 유효한 객체임을 보장
    repository = RepositoryService.get_repository_by_name_and_guid(db, reponame, gitUser.uid)
    
    if repository is None:
        repository = Repository(connectCnt=1, repoName=reponame, guid=gitUser.uid, language="")
        repository = RepositoryService.create_repository(repository, db)
    else:
        repository.connectCnt += 1
        RepositoryService.update_repository(repository, db)
    
    rtSchema = CrawlerBaseSchema(username=gitUser.username, reponame=repository.repoName)

    try:
        status = load_status(username,reponame)
        if not status.needCrawling():
            # 상태정보가 있으므로 상태정보를 반환한다
            return rtSchema
        else:
            # 상태정보가 없거나 실패했다면 크롤링을 재시작할 것
            status = save_status(username,reponame,repository.rid,WorkStatus.CRAWLING_NOW)
            background_tasks.add_task(start_crawling, repository.rid, url, db)
            return rtSchema
    except Exception as e:
        print(e)
        status = save_status(username,reponame,repository.rid,WorkStatus.CRAWLING_FAIL)
        raise HTTPException(status_code=500, detail="An error occurred while starting the crawling process.")

def start_crawling(rid: int, url: str, db: Session):
    
    sources = source_crawling(url, conv2orm)
    for source in sources:
        source.rid = rid
        SourceCodeService.create_source_code(source, db)
    
    return sources

        
def source_crawling(url: str, result_converter):
    """
    결과물을 크롤링하는 장치

    Args:
        url (str) : crawling 타겟에 대한 url
        result_converter (function) : crawling 결과물을 필요한 자료구조로 변경하는 함수

    Returns:
        result_converter에 의해서 변경된 클래스
    """

    try:
        # crawling logic
        driver = get_crawling_driver()
        crawler = GitCrawler(driver)
        crawler.start_crawl(url, ["py", "java", "js"])
        src_files = crawler.get_src_files()
        crawler.close()

        # 결과물을 원하는 객체로 convert해서 보내줌
        ret = result_converter(src_files)
        return ret

    except Exception as e:
        print("exception", e)
        raise e

