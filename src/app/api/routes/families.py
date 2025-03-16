from fastapi import APIRouter
from app.api.tags import Tags
from app.core.security.depends import CurrentSessionDep
from app.services.families import FamiliesService
from app.schemas.families import FamilyCreateSchema, FamilyPublicSchema, FamilyDBSchema
from app.core.db.depends import DbDep
from app.exceptions import ResourceNotFound
from app.schemas.pagination import ListResource
from app.depends.pagination import PaginationParamsQuery


router = APIRouter(
    prefix="/families",
    tags=[Tags.families],
)

FamilyNotFound = {
    "description": "Family not found.",
    "model": ResourceNotFound.schema(),
}


@router.get(
    "/",
    summary="List families.",
    response_model=ListResource[FamilyPublicSchema],
)
def list(
    db: DbDep, current_session: CurrentSessionDep, pagination: PaginationParamsQuery
) -> ListResource[FamilyPublicSchema]:
    """List families."""

    service = FamiliesService(db)

    results, count = service.list(pagination)

    return ListResource.from_paginated_results(
        [FamilyPublicSchema.model_validate(result) for result in results],
        count,
        pagination,
    )


@router.get(
    "/{family_id}",
    summary="Get a family by ID.",
    response_model=FamilyPublicSchema,
    responses={404: FamilyNotFound},
)
def get(
    db: DbDep, current_session: CurrentSessionDep, family_id: int
) -> FamilyPublicSchema:
    """Get a family by ID."""

    service = FamiliesService(db)

    family = service.get(family_id)

    if not family:
        raise ResourceNotFound()

    return FamilyPublicSchema.model_validate(family)


@router.post(
    "/",
    summary="Create a new family.",
    status_code=201,
    response_model=FamilyDBSchema,
    responses={201: {"description": "Family created."}},
)
def create(
    db: DbDep, current_session: CurrentSessionDep, family: FamilyCreateSchema
) -> FamilyDBSchema:
    """Create a new family."""

    service = FamiliesService(db)

    created_family = service.create(family, current_session.user)

    return FamilyDBSchema.model_validate(created_family)
