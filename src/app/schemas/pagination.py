import math
from typing import Any, Generic, NamedTuple, Self, Sequence, TypeVar
from app.schemas.base import Schema

T = TypeVar("T", bound=Any)


class PaginationParams(NamedTuple):
    page: int
    limit: int


class Pagination(Schema):
    total_count: int
    max_page: int


class ListResource(Schema, Generic[T]):
    items: list[T]
    pagination: Pagination

    @classmethod
    def from_paginated_results(
        cls, items: Sequence[T], total_count: int, pagination_params: PaginationParams
    ) -> Self:
        return cls(
            items=list(items),
            pagination=Pagination(
                total_count=total_count,
                max_page=math.ceil(total_count / pagination_params.limit),
            ),
        )
