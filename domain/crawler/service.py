from fastapi import BackgroundTasks
from sqlalchemy.orm import Session


from default.config.crawlerconfig import get_crawling_driver
from domain.crawler.crawler import GitCrawler
from domain.user.model import GithubUser
from domain.user import service as GithubUserService
from domain.repository.model import Repository
from domain.repository import service as RepositoryService
from domain.sourcecode.model import SourceCode
from domain.sourcecode import service as SourceCodeService
from domain.crawler.OrmConverter import conv2orm



async def start_crawling(username: str, reponame: str, url: str, db: Session, background_tasks: BackgroundTasks):
    gitUser = GithubUserService.get_user_by_username(db, username)
        
        # gitUser가 None인 경우 새로운 사용자를 생성
    if gitUser is None:
        gitUser = GithubUser(username=username, site=url, connectCnt=1, follower=0, following=0)
        print("fornt type: ",type(gitUser))
        gitUser = GithubUserService.create_user(gitUser, db)

    # 이제 gitUser는 반드시 유효한 객체임을 보장
    repository = RepositoryService.get_repository_by_name_and_guid(db, reponame, gitUser.uid)
    
    if repository is None:
        repository = Repository(connectCnt=1, repoName=reponame, guid=gitUser.uid, language="")
        repository = RepositoryService.create_repository(repository, db)

    sources = git_crawling(url, conv2orm)
    for source in sources:
        source.rid = repository.rid
        dbsourc = SourceCodeService.create_source_code(source, db)

        
def git_crawling(url: str, result_converter):
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

