from fastapi import APIRouter

from backend.database.db import (
    get_recent
)


router = APIRouter(
    prefix="/api",
    tags=["History"]
)


@router.get(
    "/history"
)
def history(
    limit: int = 20
):

    limit = max(
        1,
        min(
            limit,
            100
        )
    )

    return {
        "items": get_recent(
            limit
        )
    }
