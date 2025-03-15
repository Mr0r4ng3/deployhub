from typing import Any, Sequence
from sqlalchemy.orm import Session
from sqlalchemy import Select, func, over
from app.schemas.pagination import PaginationParams


def paginate(
    session: Session, statement: Select[Any], pagination: PaginationParams
) -> tuple[Sequence[Any], int]:
    page, limit = pagination
    offset = (page - 1) * limit
    statement = statement.offset(offset).limit(limit)

    statement = statement.add_columns(over(func.count()))
    result = session.execute(statement)
    results: list[Any] = []
    count = 0

    for row in result.unique().all():
        (*queried_data, c) = row._tuple()
        count = int(c)
        if len(queried_data) == 1:
            results.append(queried_data[0])
        else:
            results.append(queried_data)

    return results, count
