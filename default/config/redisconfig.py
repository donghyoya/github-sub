from pydantic import BaseSetting
import redis

class RedisConfig(BaseSetting):
    redis_host: str ="localhost"
    redis_port: int = 6379
    redis_db: int = 0

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'

    class RedisClient:
        _instance = None

        @classmethod
        def get_instance(cls):
            if cls._instance is None:
                config = RedisConfig()
                cls._instance = redis.Redis(
                    host=config.redis_host,
                    port=config.redis_port,
                    db=config.redis_db,
                    decode_responses=True
                )
            return cls._instance