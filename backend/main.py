from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api.analyze import router as analyze_router
from backend.api.history import router as history_router
from backend.api.dashboard import router as dashboard_router
from backend.rag.knowledge_base import knowledge_base
from backend.database.db import init_db

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"

app = FastAPI(
    title="NLPShield",
    description="AI/NLP Cyber Threat & Toxicity Analyzer",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(analyze_router)
app.include_router(history_router)
app.include_router(dashboard_router)

init_db()


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "NLPShield"
    }


@app.get("/api/knowledge")
def get_knowledge():
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


app.mount(
    "/",
    StaticFiles(
        directory=str(FRONTEND),
        html=True
    ),
    name="frontend"
)
