from fastapi import FastAPI

from .api import router
from .test_setup import fill_db
from .settings import RUN_MODE, RunMode


if RUN_MODE == RunMode.DEV:
    fill_db()

app = FastAPI()
app.include_router(router)
