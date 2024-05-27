import re
import time
from contextlib import contextmanager

from fastapi import BackgroundTasks

from default.config.crawlerconfig import get_crawling_driver
from default.config import dbconfig

from domain.crawler.service import source_crawling
from domain.frontend.mock_repository import add_repository, find_repository
from domain.frontend.view_model import VMRepository, VMSourceCode
from domain.frontend.converter import convert_to_vm

from domain.frontend.status_service import WorkStatus, \
    load_status, save_status, RepositoryWorkingStatus

def get_row_repository(username, reponame):
    ret = find_repository(username, reponame)
    # print("get_row ret: ",ret)
    return ret

def get_repository(username, reponame):
    ret = find_repository(username, reponame)
    # print("ret get_reposi ",ret)
    return ret

def mock_polling(username:str, reponame:str):
    """
    상태정보 가져와서 리턴
    """
    return find_repository(username, reponame)

def mock_crawl_start(background_tasks: BackgroundTasks, username: str, reponame: str, url: str):
    """
        요청한 username/reponame을 바탕으로 상태정보를 추출한다.
        상태정보가 없거나 실패했다면 크롤링을 재시작할 것
        상태정보가 있다면 상태정보를 반환한다
    """
    try:
        repo = find_repository(username,reponame)
        if repo is not None and repo['status'] != "FAIL":
            # 상태정보가 있으므로 상태정보를 반환한다
            return repo
        else:
            # 상태정보가 없거나 실패했다면 크롤링을 재시작할 것
            repo = VMRepository().set_status("WORKING").set_username(username).set_reponame(reponame)
            add_repository(username, reponame, repo)
            background_tasks.add_task(mock_crawl_service, username, reponame, url)
            return repo
    except Exception as e:
        print(e)

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
        repo = find_repository(username,reponame)
        if repo is not None and repo['status'] == "CRAWLING_COMPLETE":
            # 상태정보가 크롤링 완료면 AI 작업을 시작함
            repository = VMRepository().from_dict(repo)
            repository.set_status("AI_WORKING")
            background_tasks.add_task(mock_ai_service, username, reponame)
            add_repository(username, reponame, repository)
            return repository
        elif repo is None:
            # 상태정보가 없으면 FAIL을 붙여서 반환한다
            repository = VMRepository().set_status("FAIL").set_username(username).set_reponame(reponame)
            return repository
        else:
            # 상태정보가 있는데 그 외의 상황이면 그냥 그대로 반환한다
            return repo
    except Exception as e:
        print(e)


def mock_ai_service(username: str, reponame: str):
    """
    mock service니까 적당히 sleep하고 상태정보만 대충 바꾸고 반환
    """
    try:
        print("Start Sleep")
        time.sleep(30)
        print("End sleep")
        repo = find_repository(username,reponame)
        repo = VMRepository().from_dict(repo)
        repo.set_status("AI_COMPLETE")
        repo.set_ai_score("F").set_ai_answer("AI가 작성한 코멘트가 들어올 위치입니다.")
        add_repository(username,reponame, repo)
    except:
        repo = find_repository(username,reponame)
        repo = VMRepository().from_dict(repo)
        repo.set_status("FAIL")
        add_repository(username,reponame, repo)


