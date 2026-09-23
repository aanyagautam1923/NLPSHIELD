from pathlib import Path
import os

ROOT = Path(__file__).resolve().parent

BACKEND_DIR = ROOT / "backend"
DATASETS_DIR = ROOT / "datasets"
TRAINED_MODELS_DIR = ROOT / "trained_models"
KNOWLEDGE_BASE_DIR = ROOT / "knowledge_base"
VECTORSTORE_DIR = ROOT / "vectorstore"
DATABASE_DIR = ROOT / "database"
UPLOADS_DIR = ROOT / "uploads"
REPORTS_DIR = ROOT / "reports"
LOGS_DIR = ROOT / "logs"
FRONTEND_DIR = ROOT / "frontend"

DB_PATH = DATABASE_DIR / "nlp_shield.db"

TOXICITY_MODEL_PATH = TRAINED_MODELS_DIR / "toxicity_model.joblib"
THREAT_MODEL_PATH = TRAINED_MODELS_DIR / "threat_model.joblib"
THREAT_EXAMPLES_PATH = TRAINED_MODELS_DIR / "threat_examples.joblib"

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "qwen2.5:3b"
)

MAX_TEXT_LENGTH = 5000
RAG_TOP_K = 5

for directory in [
    TRAINED_MODELS_DIR,
    KNOWLEDGE_BASE_DIR,
    VECTORSTORE_DIR,
    DATABASE_DIR,
    UPLOADS_DIR,
    REPORTS_DIR,
    LOGS_DIR,
]:
    directory.mkdir(parents=True, exist_ok=True)
