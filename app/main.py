from fastapi import FastAPI, APIRouter

from app.controllers import (
    login_router,
    restaurant_router,
    user_router,
    area_router,
    order_router,
)
from app.config import RUN_MODE, RunMode, API_V1_PREFIX


api = APIRouter(prefix=API_V1_PREFIX)

api.include_router(login_router)
api.include_router(user_router)
api.include_router(restaurant_router)
api.include_router(area_router)
api.include_router(order_router)

app = FastAPI()
app.include_router(api)
