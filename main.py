from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

#도메인 적용
from domain.user.router import router as user_router
from domain.chatgpt.router import router as chatgpt_router
from domain.airesult.router import router as airesult_router
from domain.repository.router import router as repo_router
from domain.sourcecode.router import router as sourcecode_router
from domain.crawler.router import router as crawler_router
from domain.frontend.router import router as frontend_router

#미들웨어 적용
from default.middleware.coresmiddleware import setup_cors
from default.middleware.redismiddleware import redis_middleware

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

#표준 fastpi 미들웨어 추가
setup_cors(app)
app.middleware("http")(redis_middleware)

'''
미들웨어 차이점 검색해보기
redis_middleware(app)
app.add_middleware(redis_middleware)
'''

app.include_router(user_router,prefix="/user")
app.include_router(chatgpt_router,prefix="/chatgpt")
app.include_router(airesult_router,prefix="/airesult")
app.include_router(repo_router, prefix="/repo")
app.include_router(sourcecode_router, prefix="/source")
app.include_router(crawler_router, prefix="/crawler")
app.include_router(frontend_router, prefix="/ui")
