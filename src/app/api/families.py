from fastapi import APIRouter
from app.api.tags import Tags


router = APIRouter(
    prefix="/families",
    tags=[Tags.families],
)


@router.get("/")
async def get_families():
    return {"route": "families", "method": "GET"}


@router.post("/")
async def create_family():
    return {"route": "families", "method": "POST"}
