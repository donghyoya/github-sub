from fastapi import Request
import redis

# Redis 클라이언트 초기화
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

async def redis_middleware(request: Request, call_next):
    # 미들웨어를 적용하지 않을 경로 목록
    exclude_paths = ["/api/skipredis", "/api/anotherpath"]

    # 현재 요청 경로가 제외 목록에 있는지 확인
    if request.url.path not in exclude_paths:
        # Redis에서 특정 키 값을 가져오기
        some_key_value = redis_client.get('some_key')
        # request 상태에 값 저장
        request.state.some_key = some_key_value

    # 요청을 다음 미들웨어 또는 엔드포인트로 전달
    response = await call_next(request)
    return response
