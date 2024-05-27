from enum import Enum

from default.config.redisdbconfig import get_redis


class WorkStatus(Enum):
    NONE = "NONE"
    CRAWLING_NOW = "CRAWLING_NOW"
    CRAWLING_SUCCESS = "CRAWLING_SUCCESS"
    CRAWLING_FAIL = "CRAWLING_FAIL"
    AI_API_NOW = "AI_API_NOW"
    AI_API_SUCCESS = "AI_API_SUCCESS"
    AI_API_FAIL = "AI_API_FAIL"
    EXCEPTION = "EXCEPTION"

    def needCrawling(self):
        """
            status를 체크해서
        """
        return self in [WorkStatus.NONE, WorkStatus.CRAWLING_FAIL]

    def needAiApi(self):
        return self in [WorkStatus.AI_API_FAIL, WorkStatus.CRAWLING_SUCCESS]

    @classmethod
    def from_string(cls, string):
        for status in cls:
            if status.value == string.upper():
                return status
        raise WorkStatus.NONE

class RepositoryWorkingStatus:
    def __init__(self):
        self.username = None
        self.reponame = None
        self.status = None

    def set_usernamae(self, username: str):
        self.username = username
        return self

    def set_reponame(self, reponame: str):
        self.reponame = reponame
        return self

    def set_status(self, status: WorkStatus):
        self.status = status
        return self

    def get_cache_key(self):
        return f"{self.usernamae}:{self.reponame}:status"

    def get_cache_value(self):
        return self.status.value.encode("utf-8")

    def set_cache_value(self, data):
        self.status = WorkStatus.from_string(data.decode('utf-8'))
        return self

    def needCrawling(self):
        """
            status를 체크해서
        """
        return self.status in [WorkStatus.NONE, WorkStatus.CRAWLING_FAIL]

    def needAiApi(self):
        return self.status in [WorkStatus.AI_API_FAIL, WorkStatus.CRAWLING_SUCCESS]

def save_status(username, reponame, status:WorkStatus):
    db = get_redis()
    key = f"{username}:{reponame}:status"
    value = status.value.encode('utf-8')
    expire_seconds = 60*60
    db.setex(
        key,
        expire_seconds,
        value
    )
    status = RepositoryWorkingStatus().set_usernamae(username).set_reponame(reponame).set_status(status)
    return status

def load_status(username, reponame)->RepositoryWorkingStatus:
    db = get_redis()
    key = f"{username}:{reponame}:status"
    value = db.get(key)
    status = RepositoryWorkingStatus().set_usernamae(username).set_reponame(reponame)
    if value is None:
        status.set_status(WorkStatus.NONE)
    else:
        status.set_cache_value(value)
    return status