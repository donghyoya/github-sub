from fastapi import BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from default.config.crawlerconfig import get_crawling_driver
from default.utils.redisutils import WorkStatus, load_status, save_status, RepositoryWorkingStatus

from .crawler import GitCrawler
from .OrmConverter import conv2orm
from default.schema.cralwerschema import CrawlerBaseSchema
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
    
    # repository 없으면 False 있으면 True
    # -> sourcecode 동작 다르게
    check_repository = False
    if repository is None:
        repository = Repository(connectCnt=1, repoName=reponame, guid=gitUser.uid, language="")
        repository = RepositoryService.create_repository(repository, db)
    else:
        repository.connectCnt += 1
        RepositoryService.update_repository(repository, db)
        check_repository = True
    
    rtSchema = CrawlerBaseSchema(username=gitUser.username, reponame=repository.repoName)

    try:
        status = load_status(username,reponame)
        if not status.needCrawling():
            # 상태정보가 있으므로 상태정보를 반환한다
            return status, rtSchema
        else:
            # 상태정보가 없거나 실패했다면 크롤링을 재시작할 것
            status = save_status(username,reponame,repository.rid,WorkStatus.CRAWLING_NOW)

            if(check_repository is False):
                background_tasks.add_task(start_add_crawling, repository, url, db)
            else:
                background_tasks.add_task(start_update_crawling, repository, url, db)
            
            return status, rtSchema
    except Exception as e:
        print(e)
        status = save_status(username,reponame,repository.rid,WorkStatus.CRAWLING_FAIL)
        return status, rtSchema

'''
repository가 없는경우에 SourceCode 추가
'''
def start_add_crawling(repository: Repository, url: str, db: Session) -> List[SourceCode]:
    sources = source_crawling(url, conv2orm)

    update_sources = SourceCodeService.add_source_codes(source_codes=sources,repository=repository,db=db)

    ## 성공시 상태정보 저장
    status = save_status(repository.github_user.username, repository.repoName, repository.rid, WorkStatus.CRAWLING_SUCCESS)

    return update_sources

'''
repository가 있는경우 SourceCode 업데이트 및 추가
'''
def start_update_crawling(repository: Repository, url: str, db: Session):
    before_sources = SourceCodeService.get_all_source_codes_by_rid(rid=repository.rid, db=db)

    sources = source_crawling(url, conv2orm)

    after_sources = SourceCodeService.add_or_update_source_codes(source_codes=sources, repository=repository, db=db)

    # 리스트를 집합으로 변환하고
    before_sids = {source.sid for source in before_sources}
    after_sids = {source.sid for source in after_sources}

    #변한 집합끼리 뺄셈 연산
    missing_sids = list(before_sids - after_sids)

    SourceCodeService.update_rmstate_for_missing_sids(missing_sids=missing_sids, db=db)

    ## 성공시 상태정보 저장
    status = save_status(repository.github_user.username, repository.repoName, repository.rid, WorkStatus.CRAWLING_SUCCESS)

    return after_sources



        
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
        crawler.start_crawl(url)
        src_files = crawler.get_src_files()
        crawler.close()

        # 결과물을 원하는 객체로 convert해서 보내줌
        ret = result_converter(src_files)
        return ret

    except Exception as e:
        print("exception", e)
        raise e

