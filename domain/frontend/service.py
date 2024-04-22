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
