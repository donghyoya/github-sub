from fastapi import Request
import redis

# Redis 클라이언트 초기화
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

async def redis_middleware(request: Request, call_next):
    some_key_value = redis_client.get('some_key')
    request.state.some_key = some_key_value
    response = await call_next(request)
    return response
