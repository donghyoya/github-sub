from fastapi import FastAPI

#도메인 적용
from domain.user import router as user_router
from domain.chatgpt import router as chatgpt_router
from domain.airesult import router as airesult_router
from domain.repository import router as repo_router
from domain.sourcecode import router as sourcecode_router

#미들웨어 적용
from default.middleware.coresmiddleware import setup_cors

app = FastAPI()

setup_cors(app)

app.include_router(user_router,"/user")
app.include_router(chatgpt_router,"/chatgpt")
app.include_router(airesult_router,"/airesult")
app.include_router(repo_router, "/repo")
app.include_router(sourcecode_router, "/source")
