from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.routing import APIRoute
from app.core.config import settings
from app.api.main import api_router
from app.core.db.database import get_db
from app.core.security.schemas.users import UserCreateSchema
from app.core.security.routes import security_router
from app.core.security.services.user import UserService


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    db = next(get_db())

    user_service = UserService(db)

    if not user_service.get_by_username(settings.FIRST_SUPERUSER_USERNAME):
        user_service.create(
            UserCreateSchema(
                username=settings.FIRST_SUPERUSER_USERNAME,
                name=settings.FIRST_SUPERUSER_NAME,
                password=settings.FIRST_SUPERUSER_PASSWORD,
            )
        )

    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(security_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
