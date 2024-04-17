from fastapi import FastAPI

#도메인 적용
from domain.user.router import router as user_router
from domain.chatgpt.router import router as chatgpt_router
from domain.airesult.router import router as airesult_router
from domain.repository.router import router as repo_router
from domain.sourcecode.router import router as sourcecode_router

#미들웨어 적용
from default.middleware.coresmiddleware import setup_cors

app = FastAPI()

setup_cors(app)

app.include_router(user_router,prefix="/user")
app.include_router(chatgpt_router,prefix="/chatgpt")
app.include_router(airesult_router,prefix="/airesult")
app.include_router(repo_router, prefix="/repo")
app.include_router(sourcecode_router, prefix="/source")
