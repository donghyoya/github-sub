from enum import Enum
import json

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
        self.repoid = None

    def set_usernamae(self, username: str):
        self.username = username
        return self

    def set_reponame(self, reponame: str):
        self.reponame = reponame
        return self

    def set_status(self, status: WorkStatus):
        self.status = status
        return self
    
    def set_repoid(self, rid: int):
        self.repoid = rid
        return self
    def get_repoid(self):
        return self.repoid

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

    def to_json(self):
        data = self.__dict__.copy()
        data['status'] = self.status.value
        return json.dumps(data)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        obj = cls()
        obj.username = data.get('username')
        obj.reponame = data.get('reponame')
        obj.status = WorkStatus.from_string(data.get('status'))
        obj.repoid = data.get('repoid')
        return obj

    @classmethod
    def from_redis(cls, username: str, reponame: str):
        db = get_redis()
        key = f"{username}:{reponame}:status"
        value = db.get(key)
        if value is None:
            return cls().set_usernamae(username).set_reponame(reponame).set_status(WorkStatus.NONE)
        return cls.from_json(value.decode('utf-8'))

    @classmethod
    def from_redis(cls, rid: int):
        db = get_redis()
        key = f"{rid}:status"
        value = db.get(key)
        if value is None:
            return cls().set_repoid(rid).set_status(WorkStatus.NONE)
        return cls.from_json(value.decode('utf-8'))


def save_status(username, reponame, rid, status: WorkStatus):
    db = get_redis()
    key = f"{rid}:status"
    repo_status = RepositoryWorkingStatus().set_usernamae(username).set_reponame(reponame).set_repoid(rid).set_status(status)
    value = repo_status.to_json()
    expire_seconds = 60*60 # 1hour
    db.setex(
        key,
        expire_seconds,
        value
    )
    return repo_status

def load_status(rid: int) -> RepositoryWorkingStatus:
    return RepositoryWorkingStatus.from_redis(rid)

