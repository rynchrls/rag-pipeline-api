from math import ceil
from typing import Any


def paginate(total_docs: int, page: int, limit: int, current_fetched: int):
    total_pages = ceil(total_docs / limit) if limit else 1
    has_next = (page + 1) * limit < total_docs
    has_prev = page > 0

    paginated: dict[str, Any] = {
        "total": total_docs,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "has_next": has_next,
        "has_prev": has_prev,
        "count": current_fetched,
    }

    return paginated
