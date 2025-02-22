from fastapi import APIRouter
from app.api.families import router as families_router


main_router = APIRouter()

main_router.include_router(families_router)