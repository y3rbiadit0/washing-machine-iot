from fastapi import APIRouter

from .login import router as login_router
from .washing_machines import router as washing_machines_router

api_router = APIRouter()
api_router.include_router(login_router)
api_router.include_router(washing_machines_router)
