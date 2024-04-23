import redis
from default.config.redisconfig import RedisConfig
import json

from domain.frontend.view_model import VMRepository, VMSourceCode


class RedisClient:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = redis.Redis(
                host="localhost",
                port=6379,
                db=0,
                decode_responses=True
            )
        return cls._instance

def add_repository(username, reponame, repository):
    # db = RedisConfig.RedisClient.get_instance()
    db = RedisClient.get_instance()
    data = json.dumps(repository.to_dict(), ensure_ascii=False).encode("utf-8")
    db.set(f"{username}:{reponame}", data)

def find_repository(username, reponame):
    # db = RedisConfig.RedisClient.get_instance()
    db = RedisClient.get_instance()
    data = db.get(f"{username}:{reponame}")

    if data is not None:
        return json.loads(data)
    else:
        return None

if __name__ == "__main__":
    username = "123"
    reponame = "456"
    status = "FAIL"
    repo = VMRepository().set_username(username).set_reponame(reponame).set_status(status)
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