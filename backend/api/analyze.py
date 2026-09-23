from fastapi import (
    APIRouter,
    HTTPException
)

from pydantic import (
    BaseModel,
    Field
)

from backend.services.analysis_service import (
    analyze_text
)

from backend.database.db import (
    save_analysis
)


router = APIRouter(
    prefix="/api",
    tags=["Analysis"]
)


class AnalyzeRequest(
    BaseModel
):

    text: str = Field(
        min_length=1,
        max_length=5000
    )


@router.post(
    "/analyze"
)
def analyze(
    request: AnalyzeRequest
):

    try:

        result = analyze_text(
            request.text
        )

        save_analysis(
            request.text,
            result
        )

        return result

    except FileNotFoundError as error:

        raise HTTPException(
            status_code=503,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
