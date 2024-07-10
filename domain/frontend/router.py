from fastapi import APIRouter, Request, BackgroundTasks, Depends, HTTPException
from fastapi.templating import Jinja2Templates

from default.config.aiconfig import AiConfig
from domain.airesult.router import get_db, get_ai
from domain.frontend.schema import RepositoryForm, RequestAiForm
from domain.frontend.service import search_repository_by_rid, get_working_status, create_repository_ai_result, \
    get_ai_result_by_rid
from default.utils.urlutils import url_checker
from sqlalchemy.orm import Session

router = APIRouter(
    tags=["frontend"]
)
templates = Jinja2Templates(directory="templates")

@router.get("/")
def get_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

### rid

@router.get("/polling/{rid}")
def get_polling(rid: int):
    status = get_working_status(rid)
    return status

@router.get("/{rid}/row")
def get_repository_for_ai(
        rid: int,
        request: Request,
        db: Session = Depends(get_db),
    ):
    """
    open ai의 url query를 위해 크롤링 데이터만 보여주는 정적 페이지 return
    """
    repository = search_repository_by_rid(rid, db)
    context = {
        "request":request,
        "repo" : repository
    }
    return templates.TemplateResponse("row_repository.html", context)

@router.get("/{rid}")
def get_repository_for_user(
        rid:int,
        request:Request,
        db: Session = Depends(get_db),
    ):
    repository = search_repository_by_rid(rid, db)
    context = {
        "request": request,
        "repo": repository
    }
    return templates.TemplateResponse("result.html", context)

@router.post("/{rid}/ai")
def post_repository_ai(
        rid:int,
        request: Request,
        db: Session = Depends(get_db),
        ai_config: AiConfig = Depends(get_ai)
    ):
    ai_result = create_repository_ai_result(rid=rid, ai_config=ai_config, db=db)
    return ai_result

@router.get("/{rid}/ai")
def get_repository_ai_answer(
        rid:int,
        request: Request,
        db: Session = Depends(get_db)
    ):
    return get_ai_result_by_rid(rid, db)

# start of /frag
@router.get("/frag/{rid}/source")
def get_repository_for_user(
        rid: int,
        request:Request,
        db: Session = Depends(get_db),
    ):
    """
    javascript에서 data binding 하기 곤란하므로 server side에서 rendering된 html 조각을 제공
    """
    repository = search_repository_by_rid(rid, db)
    context = {
        "request": request,
        "repo": repository
    }
    return templates.TemplateResponse("fragment/source_code.html", context)

@router.get("/frag/{rid}/ai")
def get_repository_for_user(
        rid: int,
        request: Request,
        db: Session = Depends(get_db),
    ):
    """
    javascript에서 data binding 하기 곤란하므로 server side에서 rendering된 html 조각을 제공
    """
    repository = search_repository_by_rid(rid, db)
    context = {
        "request": request,
        "repo": repository
    }
    return templates.TemplateResponse("fragment/ai_result.html", context)

@router.get("/frag/{rid}/repository")
def get_repository_for_user(
        rid: int,
        request: Request,
        db: Session = Depends(get_db),
):
    """
    javascript에서 data binding 하기 곤란하므로 server side에서 rendering된 html 조각을 제공
    """
    repository = search_repository_by_rid(rid, db)
    context = {
        "request": request,
        "repo": repository
    }
    return templates.TemplateResponse("fragment/repository_header.html", context)
