import json

import redis

class RedisStatusRepository:
    def __init__(self):
        self.conn = redis.Redis(
            host='localhost',
            port=6379,
            db=0
        )

    def findStatusById(self, id: tuple):
        key = "{}:{}".format(*id)
        status = self.conn.get(key)
        if status is not None:
            return status.decode()
        else:
            return None

    def saveStatusById(self, id: tuple, status:str):
        key = "{}:{}".format(*id)
        self.conn.set(key, status)

if __name__ == '__main__':
    repository = RedisStatusRepository()
    id = ("username", "reponame")
    repository.saveStatusById(id, "WORKING")
    status = repository.findStatusById(id)
    if status is not None:
        print(status)

    repository.saveStatusById(id, "DONE")
    status = repository.findStatusById(id)
    if status is not None:
        print(status)

