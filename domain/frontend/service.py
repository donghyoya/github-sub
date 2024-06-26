import time
from fastapi import BackgroundTasks
from default.utils.redisutils import load_status, save_status, WorkStatus, RepositoryWorkingStatus

from domain.crawler.service import source_crawling
from domain.frontend.mock_repository import add_repository, find_repository
from domain.frontend.view_model import VMRepository, VMSourceCode
from domain.frontend.converter import convert_to_vm
from domain.repository.model import Repository
from domain.repository.service import get_repository
from sqlalchemy.orm import Session

from domain.sourcecode.model import SourceCode


def convert_repository(repository: Repository) -> VMRepository:
    vm_repo = VMRepository()
    # vm_repo.set_username(repository.github_user.username)
    (vm_repo
        .set_repoid(repository.rid)
        .set_reponame(repository.repoName)
        .set_ai_answer(repository.ai_results.answer)
        .set_ai_score(repository.ai_results.score)
    )
    source_codes = []
    for source in repository.source_codes:
        source_codes.append(convert_source_code(source))
    vm_repo.set_sources(source_codes)
    return vm_repo

def convert_source_code(source_code: SourceCode) -> VMSourceCode:
    return (VMSourceCode()
            .set_sourceName(source_code.sourceName)
            .set_sourceCode(source_code.sourceCode)
            .set_url(source_code.url)
            .set_language(source_code.language)
            .set_path(source_code.path)
        )

def search_repository_by_rid(rid, db: Session) -> VMRepository:
    repository = get_repository(rid, db)
    ret = convert_repository(repository)
    return ret

def get_working_status(username: str, reponame: str):
    return load_status(username, reponame)

def get_working_status(rid: int):
    return load_status(rid)


def mock_crawl_start(background_tasks: BackgroundTasks, username: str, reponame: str, url: str):
    """
        요청한 username/reponame을 바탕으로 상태정보를 추출한다.
        상태정보가 없거나 실패했다면 크롤링을 재시작할 것
        상태정보가 있다면 상태정보를 반환한다
    """
    try:
        status = load_status(username,reponame)
        if not status.needCrawling():
            # 상태정보가 있으므로 상태정보를 반환한다
            return status
        else:
            # 상태정보가 없거나 실패했다면 크롤링을 재시작할 것
            status = save_status(username,reponame,WorkStatus.CRAWLING_NOW)
            background_tasks.add_task(mock_crawl_service, username, reponame, url)
            return status
    except Exception as e:
        print(e)
        status = save_status(username,reponame,WorkStatus.CRAWLING_FAIL)
        return status

def mock_crawl_service(username: str, reponame: str, url: str):
    """
    임시로 만든 크롤링 작업 시작 서비스
    크롤러 도메인을 사용하여 크롤링 작업을 시작한다
    상태정보를 변경한다
    """
    try:
        # 크롤링 업무
        sources = source_crawling(url, convert_to_vm)

        # 데이터베이스에 저장
        repo = VMRepository().set_username(username).set_reponame(reponame)
        repo.set_sources(sources)
        add_repository(username,reponame, repo)

        # 상태정보 저장 - 성공
        save_status(username,reponame, WorkStatus.CRAWLING_SUCCESS)
    except Exception as e:
        print("exception", e)
        # 상태정보 저장 - 실패
        save_status(username,reponame, WorkStatus.CRAWLING_FAIL)

def mock_ai_start(background_tasks: BackgroundTasks, username: str, reponame: str):
    """
        상태정보를 확인하고 ai 작업을 시작한다.
        상태정보가 '크롤링 완료'인 경우에만 AI작업을 시작한다
    """
    try:
        # 상태정보 확인
        status = load_status(username,reponame)

        if status.needAiApi():
            # 상태정보가 크롤링 완료면 AI 작업을 시작함
            status = save_status(username,reponame, WorkStatus.AI_API_NOW)
            background_tasks.add_task(mock_ai_service, username, reponame)
            return status
        else:
            return status
    except Exception as e:
        status = save_status(username,reponame, WorkStatus.AI_API_FAIL)
        return status

def mock_ai_service(username: str, reponame: str):
    """
    mock service니까 적당히 sleep하고 상태정보만 대충 바꾸고 반환
    """
    try:
        print("Start Sleep")
        time.sleep(30)
        print("End sleep")

        # Repository에 저장
        repo = find_repository(username,reponame)
        repo = VMRepository().from_dict(repo)
        repo.set_ai_score("F").set_ai_answer("AI가 작성한 코멘트가 들어올 위치입니다.")
        add_repository(username,reponame, repo)

        # 상태정보
        status = save_status(username,reponame, WorkStatus.AI_API_SUCCESS)
    except:
        status = save_status(username,reponame, WorkStatus.AI_API_FAIL)


