import time
from fastapi import BackgroundTasks, HTTPException

from default.config.aiconfig import AiConfig
from default.utils.redisutils import load_status, save_status, WorkStatus
from domain.airesult.model import AiResult
from domain.airesult.schema import AiSettingSchema, AiResultBaseSchema
from domain.airesult.service import create_ai_result

from domain.crawler.service import source_crawling
from domain.frontend.view_model import VMRepository
from domain.frontend.converter import convert_to_vm, convert_repository_to_vm
from domain.repository.service import get_repository
from sqlalchemy.orm import Session


def search_repository_by_rid(rid, db: Session) -> VMRepository:
    repository = get_repository(rid, db)
    ret = convert_repository_to_vm(repository)
    return ret

def get_working_status(rid: int):
    return load_status(rid)

# AI - SERVICE
def create_prompt(rid):
    """
        git repositoy 코드를 분석하는 AI 프롬프트 생성기
    """
    host = "localhost:8000" # ENV로 따로 만들어둘 것
    ret = f"'{host}/{rid}/row'링크는 어떤 프로젝트의 소스코드를 모아둔 것입니다. 해당 링크에 접근하여 소스코드들을 분석해주십시오."
    return ret

def create_repository_ai_result(rid:int, db: Session, ai_config: AiConfig):
    """
        repository_id를 바탕으로 AI에게 평가 생성하기
    """
    repository = get_repository(rid, db)
    if repository is None:
        # 크롤링 데이터가 없으면 404
        raise HTTPException(status_code=404)

    # 프롬프트 생성
    prompt = create_prompt(rid)

    try:
        # AI에게 질의
        completion = ai_config.chat(prompt=prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # AI 데이터를 데이터베이스에 집어넣기
    ai_setting = AiSettingSchema(model=ai_config.output_model, answer=completion)
    ai_result = insertOrUpdateAi(repository=repository, ai_setting=ai_setting, db=db)
    return ai_result

def insertOrUpdateAi(repository, ai_setting: AiSettingSchema, db: Session):
    ai_result_insert_db = AiResult(
        model = ai_setting.model,
        answer = ai_setting.answer,
        score = 50,
        rid=repository.rid,
        repository=repository
    )
    ai_resultdb = create_ai_result(ai_result_insert_db, db)
    return AiResultBaseSchema.model_validate(ai_resultdb)
