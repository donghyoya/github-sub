from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from default.config import dbconfig
from domain.frontend.service import get_row_repository, get_repository

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
    print("12345", len(repository.sources))
    for src in repository.sources:
        print(src.sourceName)
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
    print("12345", len(repository.sources))
    for src in repository.sources:
        print(src.sourceName)
    return templates.TemplateResponse("result.html", context)

