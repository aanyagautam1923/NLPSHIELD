from fastapi import APIRouter

from backend.rag.knowledge_base import knowledge_base

router = APIRouter(
    prefix="/api",
    tags=["Knowledge Base"]
)


@router.get("/knowledge")
def get_knowledge():
    documents = knowledge_base.documents

    if not knowledge_base.loaded:
        knowledge_base.load()
        documents = knowledge_base.documents

    return {
        "count": len(documents),
        "documents": [
            {
                "source": item.get("source", ""),
                "text": item.get("text", "")
            }
            for item in documents
        ]
    }
