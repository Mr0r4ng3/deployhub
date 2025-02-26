from fastapi import APIRouter, HTTPException
from app.api.tags import Tags
from app.services.families import FamiliesService
from app.models.families import FamilyCreate, FamilyPublic
from app.api.deps import DbDep


router = APIRouter(
    prefix="/families",
    tags=[Tags.families],
)


@router.get("/", response_model=list[FamilyPublic])
def get_families(db: DbDep, page: int = 1, limit: int = 10):
    service = FamiliesService(db)

    skip = (page - 1) * limit

    families = service.get_all(skip, limit)

    return [FamilyPublic.model_validate(family) for family in families]


@router.get(
    "/{family_id}",
)
def get_family(db: DbDep, family_id: int):
    service = FamiliesService(db)

    family = service.get_by_id(family_id)

    if not family:
        raise HTTPException(status_code=404, detail="Family not found")
    return FamilyPublic.model_validate(family)


@router.post("/", status_code=201, response_model=FamilyPublic)
def create_family(db: DbDep, family: FamilyCreate):
    service = FamiliesService(db)

    created_family = service.create(family)

    return FamilyPublic.model_validate(created_family)
