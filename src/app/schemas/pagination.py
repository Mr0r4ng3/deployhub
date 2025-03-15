import math
from typing import Generic, NamedTuple, Self, Sequence, TypeVar
from app.schemas.base import Schema

S = TypeVar("S", bound=Schema)


class PaginationParams(NamedTuple):
    page: int
    limit: int


class Pagination(Schema):
    total_count: int
    max_page: int


class ListResource(Schema, Generic[S]):
    items: list[S]
    pagination: Pagination

    @classmethod
    def from_paginated_results(
        cls, items: Sequence[S], total_count: int, pagination_params: PaginationParams
    ) -> Self:
        return cls(
            items=list(items),
            pagination=Pagination(
                total_count=total_count,
                max_page=math.ceil(total_count / pagination_params.limit),
            ),
        )
