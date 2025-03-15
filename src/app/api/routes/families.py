from fastapi import APIRouter, HTTPException
from app.api.tags import Tags
from app.core.security.depends import CurrentSessionDep
from app.services.families import FamiliesService
from app.schemas.families import FamilyCreateSchema, FamilyPublicSchema
from app.core.db.depends import DbDep


router = APIRouter(
    prefix="/families",
    tags=[Tags.families],
)


@router.get("/", response_model=list[FamilyPublicSchema])
def get_families(
    db: DbDep, current_session: CurrentSessionDep, page: int = 1, limit: int = 10
):
    service = FamiliesService(db)

    skip = (page - 1) * limit

    families = service.get_all(skip, limit)

    return [FamilyPublicSchema(id=family.id, name=family.name) for family in families]


@router.get(
    "/{family_id}",
)
def get_family(db: DbDep, current_session: CurrentSessionDep, family_id: int):
    service = FamiliesService(db)

    family = service.get_by_id(family_id)

    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    return FamilyPublicSchema(id=family.id, name=family.name)


@router.post("/", status_code=201, response_model=FamilyPublicSchema)
def create_family(
    db: DbDep, current_session: CurrentSessionDep, family: FamilyCreateSchema
):
    service = FamiliesService(db)

    created_family = service.create(family)

    return FamilyPublicSchema(id=created_family.id, name=created_family.name)
