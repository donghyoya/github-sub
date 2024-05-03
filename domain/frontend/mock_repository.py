import redis
from default.config.redisconfig import RedisConfig
import json

from default.config.redisdbconfig import get_redis
from domain.frontend.view_model import VMRepository, VMSourceCode
from domain.frontend.work_status import WorkStatus


def add_status_repository(username, reponame, status: WorkStatus):
    db = get_redis()
    status_key = f"{username}:{reponame}:status"
    expire_second = 60 * 60
    print(status.value)
    db.setex(status_key, expire_second, status.value)


def get_status_repository(username, reponame)->WorkStatus:
    db = get_redis()
    status_key = f"{username}:{reponame}:status"
    status = db.get(status_key)
    if status is not None:
        return WorkStatus.from_string(status.decode('utf-8'))
    else:
        return WorkStatus.NONE

def add_repository(username, reponame, repository):
    # db = RedisConfig.RedisClient.get_instance()
    db = get_redis()
    data = json.dumps(repository.to_dict(), ensure_ascii=False).encode("utf-8")
    expire_second = 60 * 60
    db.setex(f"{username}:{reponame}", expire_second, data)

def find_repository(username, reponame):
    # db = RedisConfig.RedisClient.get_instance()
    db = get_redis()
    data = db.get(f"{username}:{reponame}")

    if data is not None:
        return json.loads(data)
    else:
        return None

if __name__ == "__main__":
    username = "123"
    reponame = "456"
    repo = VMRepository().set_username(username).set_reponame(reponame).set_status(WorkStatus.CRAWLING_FAIL)
    sources = [
        VMSourceCode().set_sourceCode("a+b").set_language("py"),
        VMSourceCode().set_sourceCode("a-b").set_language("java"),
    ]
    repo.set_sources(sources)

    print(repo.to_dict())
    add_repository(username,reponame, repo)
    data = find_repository(username,reponame)
    repo.from_dict(data)
    print(repo.to_dict())