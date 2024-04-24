from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.templating import Jinja2Templates

from domain.frontend.schema import RepositoryForm
from domain.frontend.service import get_row_repository, get_repository, url_checker, mock_polling, mock_crawl_start

router = APIRouter(
    tags=["frontend"]
)
templates = Jinja2Templates(directory="templates")

@router.get("/")
def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/mock/crawl")
def post_crawl(form: RepositoryForm, background_tasks: BackgroundTasks):
    repo = url_checker(form.url)

    if repo is not None:
        background_tasks.add_task(mock_crawl_start, repo[0], repo[1], form.url)
        return {
            'status': 'success',
            'username' : repo[0],
            'reponame' : repo[1]
        }
    else:
        return {
            'status' : 'fail',
            'username' : None,
            'reponame' : None
        }

@router.get("/mock/polling/{username}/{reponame}")
def get_polling(username: str, reponame: str):
    repo = mock_polling(username, reponame)
    if repo is not None:
        return repo
    else:
        return {
            'status' : 'Not Found'
        }

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

@router.get("/{username}/{reponame}/source")
def get_repository_for_user(
        username: str, reponame: str,
        request:Request):

    repository = get_repository(username, reponame)
    context = {
        "request": request,
        "repo": repository
    }
    return templates.TemplateResponse("sourceCodeTemplate.html", context)

@router.get("/example")
def get_example(request: Request):
    return templates.TemplateResponse("example.html", {'request':request})