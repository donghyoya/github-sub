import re

from fastapi import BackgroundTasks

from domain.crawler.router import GitCrawler
from domain.frontend.mock_repository import add_repository, find_repository
from domain.frontend.view_model import VMRepository, VMSourceCode


def get_row_repository(username, reponame):
    ret = find_repository(username, reponame)
    return ret

def get_repository(username, reponame):
    ret = find_repository(username, reponame)
    return ret

def mock_polling(username:str, reponame:str):
    return find_repository(username, reponame)


def mock_crawl_start(background_tasks: BackgroundTasks, username: str, reponame: str, url: str):
    try:
        repo = find_repository(username,reponame)
        if repo is not None:
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

        crawler = GitCrawler()
        crawler.start_crawl(url, ["py", "java", "js"])
        src_files = crawler.get_src_files()

        # 결과물 저장
        sources = []
        for src in src_files:
            source = VMSourceCode()
            source.set_url(src.url)
            source.set_sourceName(src.title)
            source.set_path(src.directory)
            source.set_sourceCode(src.src)
            source.set_language(src.language)

            sources.append(source)

        repo.set_sources(sources)
        repo.set_status("CRAWLING_COMPLETE")
        add_repository(username,reponame, repo)

        crawler.close()

    except Exception as e:
        print("exception", e)
        repo.set_status("FAIL")
        add_repository(username,reponame,repo)
        crawler.close()

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
