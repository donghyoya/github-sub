from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.templating import Jinja2Templates

from domain.frontend.schema import RepositoryForm, RequestAiForm
from domain.frontend.service import get_row_repository, get_repository, \
    mock_polling, mock_crawl_start, mock_ai_start
from default.utils.urlutils import url_checker

router = APIRouter(
    tags=["frontend"]
)
templates = Jinja2Templates(directory="templates")

@router.get("/")
def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/{username}/{reponame}/row")
def get_repository_for_ai(
        username: str, reponame: str,
        request: Request):
    """
    open ai의 url query를 위해 크롤링 데이터만 보여주는 정적 페이지 return
    """
    repository = get_row_repository(username, reponame)
    context = {
        "request":request,
        "repo" : repository
    }
    return templates.TemplateResponse("row_repository.html", context)

@router.get("/{username}/{reponame}")
def get_repository_for_user(
        username: str, reponame: str,
        request:Request):
    repository = get_repository(username, reponame)
    context = {
        "request": request,
        "repo": repository
    }
    return templates.TemplateResponse("result.html", context)

# start of /frag
@router.get("/frag/{username}/{reponame}/source")
def get_repository_for_user(
        username: str, reponame: str,
        request:Request):
    """
    javascript에서 data binding 하기 곤란하므로 server side에서 rendering된 html 조각을 제공
    """
    repository = get_repository(username, reponame)
    context = {
        "request": request,
        "repo": repository
    }
    return templates.TemplateResponse("fragment/source_code.html", context)

@router.get("/frag/{username}/{reponame}/ai")
def get_repository_for_user(
        username: str, reponame: str,
        request:Request):
    """
    javascript에서 data binding 하기 곤란하므로 server side에서 rendering된 html 조각을 제공
    """
    repository = get_repository(username, reponame)
    context = {
        "request": request,
        "repo": repository
    }
    return templates.TemplateResponse("fragment/ai_result.html", context)

@router.get("/frag/{username}/{reponame}/repository")
def get_repository_for_user(
        username: str, reponame: str,
        request:Request):
    """
    javascript에서 data binding 하기 곤란하므로 server side에서 rendering된 html 조각을 제공
    """
    repository = get_repository(username, reponame)
    context = {
        "request": request,
        "repo": repository
    }
    return templates.TemplateResponse("fragment/repository_header.html", context)

# end of /frag

# start of mock
@router.post("/mock/crawl")
def post_crawl(form: RepositoryForm, background_tasks: BackgroundTasks):
    repo = url_checker(form.url)
    if repo is not None:
        status = mock_crawl_start(background_tasks, repo[0], repo[1], form.url)
        return status
    else:
        return {
            'status' : 'FAIL'
        }

@router.get("/mock/polling/{username}/{reponame}")
def get_polling(username: str, reponame: str):
    status = mock_polling(username, reponame)
    return status

@router.post("/mock/ai")
def get_mock_ai(form: RequestAiForm, background_tasks: BackgroundTasks):
    status = mock_ai_start(background_tasks, form.username, form.reponame)
    return status

# end of mock
