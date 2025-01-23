from fastapi import FastAPI, APIRouter

from .api import router


app = FastAPI()
app.include_router(router)
