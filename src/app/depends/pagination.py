from typing import Annotated
from fastapi import Depends, Query
from app.core.config import settings
from app.schemas.pagination import PaginationParams


def get_pagination_params(
    page: int = Query(default=1, description="Page number, defaults to 1.", gt=0),
    limit: int = Query(
        default=10,
        description=(
            f"Size of a page, defaults to 10. "
            f"Maximum is {settings.API_PAGINATION_MAX_LIMIT}."
        ),
        gt=0,
    ),
) -> PaginationParams:
    return PaginationParams(page, min(settings.API_PAGINATION_MAX_LIMIT, limit))


PaginationParamsQuery = Annotated[PaginationParams, Depends(get_pagination_params)]
