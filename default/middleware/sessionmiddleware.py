import os
from dotenv import load_dotenv

from starlette.middleware.sessions import SessionMiddleware

load_dotenv(".env")

def setup_middleware(app):
    key=os.getenv("SESSION_KEY")
    app.add_middleware(SessionMiddleware, secret_key=key)