from fastapi import FastAPI
from domain.user import router as user_router


app = FastAPI()

app.include_router(user_router,"/user")