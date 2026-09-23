from fastapi import APIRouter

from backend.database.db import (
    get_recent
)


router = APIRouter(
    prefix="/api",
    tags=["Dashboard"]
)


@router.get(
    "/dashboard"
)
def dashboard():

    items = get_recent(
        1000
    )

    threats = sum(
        1
        for item in items
        if item["result"]["threat"]["threat"]
    )

    toxic = sum(
        1
        for item in items
        if item["result"]["toxicity"]["toxic"]
    )

    high_risk = sum(
        1
        for item in items
        if item["result"]["risk"] == "HIGH"
    )

    return {
        "total_analyzed": len(items),
        "threats_detected": threats,
        "toxic_messages": toxic,
        "high_risk": high_risk
    }
