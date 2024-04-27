import re

from fastapi import BackgroundTasks

from default.config.crawlerconfig import get_crawling_driver
from domain.crawler.converter import convert_to_vm
from domain.crawler.router import GitCrawler
from domain.crawler.service import git_crawling
from domain.frontend.mock_repository import add_repository, find_repository
from domain.frontend.view_model import VMRepository, VMSourceCode


def get_row_repository(username, reponame):
    ret = find_repository(username, reponame)
    return ret

def get_repository(username, reponame):
    ret = find_repository(username, reponame)
    return ret

def mock_polling(username:str, reponame:str):
    """
    상태정보 가져와서 리턴
    """
    return find_repository(username, reponame)

def mock_crawl_start(background_tasks: BackgroundTasks, username: str, reponame: str, url: str):
    """
    백그라운드에서 크롤링을 시작시키는 서비스
    """
    try:
        repo = find_repository(username,reponame)
        if repo is not None and repo['status'] != "FAIL":
            # 이미 저장된 repository가 있으면 그거 꺼내옴
            return repo
        else:
            # 그렇지 않다면 작업을 실시함
            repo = VMRepository().set_status("WORKING").set_username(username).set_reponame(reponame)
            background_tasks.add_task(mock_crawl_service, username, reponame, url)
            return repo
    except Exception as e:
        print(e)

def mock_crawl_service(username: str, reponame: str, url: str):
    repo = VMRepository().set_status("WORKING").set_username(username).set_reponame(reponame)
    try:
        add_repository(username, reponame, repo)
        sources = git_crawling(url, convert_to_vm)
        repo.set_sources(sources)
        repo.set_status("CRAWLING_COMPLETE")
        add_repository(username,reponame, repo)

    except Exception as e:
        print("exception", e)
        repo.set_status("FAIL")
        add_repository(username,reponame,repo)

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
