from fastapi import FastAPI

#도메인 적용
from domain.user.router import router as user_router
from domain.chatgpt.router import router as chatgpt_router
from domain.airesult.router import router as airesult_router
from domain.repository.router import router as repo_router
from domain.sourcecode.router import router as sourcecode_router
from domain.crawler.router import router as crawler_router

#미들웨어 적용
from default.middleware.coresmiddleware import setup_cors
from default.middleware.redismiddleware import redis_middleware

app = FastAPI()

#표준 fastpi 미들웨어 추가
app.add_middleware(setup_cors)
app.middleware("http")(redis_middleware)

'''
직접 함수를 호출하는 방식 (이 경우, 이 함수 내에서 미들웨어 로직이 app 인스턴스에 적용되어야 함)
redis_middleware(app)
'''

app.include_router(user_router,prefix="/user")
app.include_router(chatgpt_router,prefix="/chatgpt")
app.include_router(airesult_router,prefix="/airesult")
app.include_router(repo_router, prefix="/repo")
app.include_router(sourcecode_router, prefix="/source")
app.include_router(crawler_router, prefix="/crawler")
