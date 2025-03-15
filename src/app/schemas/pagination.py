import math
from app.core.db.base.models import Model
from typing import Generic, NamedTuple, Self, Sequence, TypeVar
from app.schemas.base import Schema

M = TypeVar("M", bound=Model)


class PaginationParams(NamedTuple):
    page: int
    limit: int


class Pagination(Schema):
    total_count: int
    max_page: int


class ListResource(Schema, Generic[M]):
    items: list[M]
    pagination: Pagination

    @classmethod
    def from_paginated_results(
        cls, items: Sequence[M], total_count: int, pagination_params: PaginationParams
    ) -> Self:
        return cls(
            items=list(items),
            pagination=Pagination(
                total_count=total_count,
                max_page=math.ceil(total_count / pagination_params.limit),
            ),
        )
