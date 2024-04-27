import redis
from default.config.redisconfig import RedisConfig
import json

from default.config.redisdbconfig import get_redis
from domain.frontend.view_model import VMRepository, VMSourceCode



def add_repository(username, reponame, repository):
    # db = RedisConfig.RedisClient.get_instance()
    db = get_redis()
    data = json.dumps(repository.to_dict(), ensure_ascii=False).encode("utf-8")
    db.set(f"{username}:{reponame}", data)

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