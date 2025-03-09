from fastapi.routing import APIRouter
from app.core.security.routes.auth import router as auth_router

security_router = APIRouter()

security_router.include_router(auth_router)
