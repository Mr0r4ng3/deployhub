from typing import List
from fastapi import APIRouter
from app.api.tags import Tags
from app.core.security.depends import CurrentSessionDep
from app.services.families import FamiliesService
from app.schemas.families import FamilyCreateSchema, FamilyPublicSchema
from app.core.db.depends import DbDep
from app.exceptions import ResourceNotFound


router = APIRouter(
    prefix="/families",
    tags=[Tags.families],
)

FamilyNotFound = {
    "description": "Family not found.",
    "model": ResourceNotFound.schema(),
}


@router.get("/", response_model=List[FamilyPublicSchema])
def list(db: DbDep, current_session: CurrentSessionDep, page: int = 1, limit: int = 10):
    """List families."""

    service = FamiliesService(db)

    skip = (page - 1) * limit

    families = service.get_all(skip, limit)

    return [FamilyPublicSchema(id=family.id, name=family.name) for family in families]


@router.get(
    "/{family_id}",
    response_model=FamilyPublicSchema,
    responses={404: FamilyNotFound},
)
def get(db: DbDep, current_session: CurrentSessionDep, family_id: int):
    """Get a family by ID."""

    service = FamiliesService(db)

    family = service.get_by_id(family_id)

    if not family:
        raise ResourceNotFound()

    return FamilyPublicSchema(id=family.id, name=family.name)


@router.post(
    "/",
    status_code=201,
    response_model=FamilyPublicSchema,
    summary="Create a new family.",
    responses={201: {"description": "Family created."}},
)
def create(db: DbDep, current_session: CurrentSessionDep, family: FamilyCreateSchema):
    """Create a new family."""

    service = FamiliesService(db)

    created_family = service.create(family)

    return FamilyPublicSchema(id=created_family.id, name=created_family.name)
