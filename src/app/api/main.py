from fastapi import APIRouter
from app.api.routes.families import router as families_router


api_router = APIRouter()

api_router.include_router(families_router)
