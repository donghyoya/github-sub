import redis
from dotenv import load_dotenv
import os

load_dotenv(".env")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = 0 # os.getenv("REDIS_DB")

def get_redis() -> redis.Redis:
    try:
        client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB
        )
        return client
    except :
        print("fail to connect redis")
        return None
