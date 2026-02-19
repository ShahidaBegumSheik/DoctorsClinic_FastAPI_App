from typing import Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, func


def paginate(
    db: Session,
    stmt,
    page: int = 1,
    size: int = 10,
) -> Tuple[int, list[Any]]:
    """
    Example - Give page 2 with 10 items per page

    """

    if page < 1:
        page = 1
    if size < 1:
        size = 10

    # Total count
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.execute(count_stmt).scalar_one()

    # Paged items
    items = db.execute(
        stmt.offset((page - 1) * size).limit(size)
    ).scalars().all()

    return total, items