import re

from domain.crawler.router import GitCrawler
from domain.frontend.mock_repository import add_repository, find_repository
from domain.frontend.view_model import VMRepository, VMSourceCode


def get_row_repository(username, reponame):
    """
    Get a row git repository
    - 왜냐하면 AI query를 위해서 그냥 크롤링된 데이터만 추출해서 가져오기
    """
    repo = {
        "username" : username,
        "reponame" : reponame,
        "sources" : [
            {
                "url" : "",
                "sourceName" : "plus.py",
                "path" : "src/main",
                "sourceCode" : "a+b",
                "language" : "py"
            },
            {
                "url": "",
                "sourceName": "minus.py",
                "path": "src/main",
                "sourceCode": "a-b",
                "language": "py"
            }
        ]
    }


    ret = VMRepository()
    ret.set_username(repo["username"]).set_reponame(repo["reponame"])
    sources = []
    for source in repo["sources"]:
        src = VMSourceCode()
        src.set_url(source["url"])
        src.set_sourceName(source["sourceName"])
        src.set_path(source["path"])
        src.set_sourceCode(source["sourceCode"])
        src.set_language(source["language"])
        sources.append(src)

    ret.set_sources(sources)
    return ret

def get_repository(username, reponame):
    """
    Get a row git repository
    - 왜냐하면 AI query를 위해서
    """
    repo = {
        "username" : username,
        "reponame" : reponame,
        "ai_score" : "A+",
        "ai_answer" : "이 코드는 원숭이도 작성할 수 있는 코드입니다. 다시 짜십시오",
        "sources" : [
            {
                "url" : "",
                "sourceName" : "plus.py",
                "path" : "src/main",
                "sourceCode" : "a+b",
                "language" : "py"
            },
            {
                "url": "",
                "sourceName": "minus.py",
                "path": "src/main",
                "sourceCode": "a-b",
                "language": "py"
            }
        ]
    }

    ret = VMRepository()
    ret.set_username(repo["username"]).set_reponame(repo["reponame"])
    sources = []
    for source in repo["sources"]:
        src = VMSourceCode()
        src.set_url(source["url"])
        src.set_sourceName(source["sourceName"])
        src.set_path(source["path"])
        src.set_sourceCode(source["sourceCode"])
        src.set_language(source["language"])
        sources.append(src)

    ret.set_sources(sources)
    ret.set_ai_score(repo["ai_score"])
    ret.set_ai_answer(repo["ai_answer"])
    return ret

def mock_polling(username:str, reponame:str):
    return find_repository(username, reponame)

def mock_crawl_start(username: str, reponame: str, url: str):
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
