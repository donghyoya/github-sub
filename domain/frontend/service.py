import time
from fastapi import BackgroundTasks
from default.utils.redisutils import load_status, save_status, WorkStatus

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


